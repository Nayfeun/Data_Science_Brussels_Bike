import pandas as pd
import seaborn as sns
import requests
import matplotlib.pyplot as plt
from get_one_device_measures import request_device
import argparse


def add_time_series_from_time_gap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a time series column corresponding to time gap from https://data.mobility.brussels/bike/api/counts/?request=time_gaps
    Parameters
    ----------
    df : Dataframe containing a "time_gap" column

    Returns
    -------
    Dataframe with "time_series" column
    """
    url = "https://data.mobility.brussels/bike/api/counts/?request=time_gaps&outputFormat=json"
    response = requests.get(url)
    response.json()
    time_series = []
    for value in df["time_gap"]:
        time_series.append(response.json()["data"][str(value)]["start_time"][:-3])
    df["time_series"] = pd.Series(time_series)
    return df


def display_time_series_one_device(device_id: str, start_date: str, end_date: str) -> sns.lineplot:
    """
    Display bikes time series from one device from "https://data.mobility.brussels/bike/api/counts"

    Parameters
    ----------
    device_id : Name of the device from which the data will be taken from.
    start_date : Data's starting date. Format : YYYYMMDD
    end_date : Data's ending date. Format : YYYYMMDD

    Returns
    -------
    Line plot displaying time series from one device
    """
    df = request_device(device_id, start_date, end_date)
    df = add_time_series_from_time_gap(df)

    sns.lineplot(df, x="time_series", y="count")
    plt.xlabel("Time Series")
    plt.ylabel("Counts")
    plt.title(f"Bike Time Series for Device {device_id}")
    plt.show()


def main():
    parser = argparse.ArgumentParser(prog="Bike Time Series Display", description="Display data from one device")
    parser.add_argument("device",
                        help="Select one device in this list : https://data.mobility.brussels/bike/api/counts/?request=devices&outputFormat=csv")
    parser.add_argument("start_date", help="Format : YYYYMMDD")
    parser.add_argument("end_date", help="Format : YYYYMMDD")
    args = parser.parse_args()

    display_time_series_one_device(args.device, args.start_date, args.end_date)


if __name__ == "__main__":
    main()
