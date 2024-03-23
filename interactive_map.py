import plotly.express as px
import pandas as pd
import requests
from get_all_devices_measures import request_all_devices
import argparse


def get_coordinates() -> pd.DataFrame:
    """
    Generate a pandas Dataframe with name and coordinates of all devices in Brussels.

    Returns
    -------
    Pandas Dataframe with name, longitude and latitude of all devices.
    """
    url = f"https://data.mobility.brussels/bike/api/counts/?request=devices&outputFormat=json"
    response = requests.get(url)
    df = pd.json_normalize(response.json()["features"])
    coordinates_df = df[['properties.device_name', "geometry.coordinates"]]
    coordinates_df.rename(columns={'properties.device_name': 'device_name'}, inplace=True)
    coordinates = list(zip(*coordinates_df["geometry.coordinates"]))
    coordinates_df["longitude"] = pd.Series(coordinates[0])
    coordinates_df["latitude"] = pd.Series(coordinates[1])
    coordinates_df.drop(["geometry.coordinates"], axis=1, inplace=True)
    return coordinates_df


def add_traffic(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Add mean traffic per device to a Pandas Dataframe with device names.

    Parameters
    ----------
    df : Pandas Dataframe with devices names.
    start_date : Data's starting date. Format : YYYYMMDD
    end_date : Data's ending date. Format : YYYYMMDD

    Returns
    -------
    Pandas Dataframe with devices names and mean traffic per device.
    """
    traffic_df = request_all_devices(start_date, end_date).groupby("device_name")["count"].mean()
    merged_df = pd.merge(df, traffic_df, on='device_name', how='left')
    merged_df['count'].fillna(0, inplace=True)
    merged_df.rename(columns={'count': 'daily_traffic'}, inplace=True)
    return merged_df


def traffic_map(df: pd.DataFrame):
    """
    Create a map of all devices in Brussels.
    Parameters
    ----------
    df : Pandas Dataframe with longitude, latitude, device_name and daily_traffic as columns.

    Returns
    -------
    None
    """
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="device_name",
        hover_data=["daily_traffic"],
        color="daily_traffic",
        zoom=10,
        height=300,
        width=600,

    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def main():
    parser = argparse.ArgumentParser(prog="Brussels Devices Map", description="Create a map of all devices in Brussels")
    parser.add_argument("start_date", help="Format : YYYYMMDD")
    parser.add_argument("end_date", help="Format : YYYYMMDD")
    args = parser.parse_args()
    devices_df = get_coordinates()
    devices_df = add_traffic(devices_df, start_date=args.start_date, end_date=args.end_date)
    traffic_map(devices_df)


if __name__ == "__main__":
    main()
