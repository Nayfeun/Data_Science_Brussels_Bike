import pandas as pd
import requests
from get_one_device_measures import request_device
import argparse
from pathlib import Path

url = "https://data.mobility.brussels/bike/api/counts/?request=devices&outputFormat=json"
response = requests.get(url)
response.json()

devices_list = []
for i in range(response.json()["totalFeatures"]):
    devices_list.append(response.json()["features"][i]["properties"]["device_name"])


def request_all_devices(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Request all bike data from all devices from "https://data.mobility.brussels/bike/api/counts"

    Parameters
    ----------
    start_date : Data's starting date. Format : YYYYMMDD
    end_date : Data's ending date. Format : YYYYMMDD

    Returns
    -------
    Pandas dataframe containing all data requested
    """
    all_devices_df = pd.DataFrame()
    for device in devices_list:
        device_df = request_device(device, start_date, end_date)
        device_df["device_name"] = device
        all_devices_df = pd.concat([all_devices_df, device_df])
    return all_devices_df


def main():
    parser = argparse.ArgumentParser(prog="Bike Data Request", description="Request data from all devices")
    parser.add_argument("start_date", help="Format : YYYYMMDD")
    parser.add_argument("end_date", help="Format : YYYYMMDD")
    args = parser.parse_args()
    df = request_all_devices(args.start_date, args.end_date)
    path = Path(f"data/ALL_DEVICES_{args.start_date}_{args.end_date}.parquet")
    df.to_parquet(path)


if __name__ == "__main__":
    main()
