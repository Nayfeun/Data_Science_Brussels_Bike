from pathlib import Path
import pandas as pd
import requests
import datetime as dt
import sys
import argparse


def request_device(device_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Request all bike data from one device from "https://data.mobility.brussels/bike/api/counts"

    Parameters
    ----------
    device_id : Name of the device from which the data will be gathered.
    start_date : Data's starting date. Format : YYYYMMDD
    end_date : Data's ending date. Format : YYYYMMDD

    Returns
    -------
    Pandas dataframe containing all data requested
    """
    url = f"https://data.mobility.brussels/bike/api/counts/?request=history&featureID={device_id}&startDate={start_date}&endDate={end_date}&outputFormat=json"
    response = requests.get(url)
    response.json()["data"]
    print(pd.json_normalize(response.json()["data"]))
    return pd.json_normalize(response.json()["data"])


def main():
    parser = argparse.ArgumentParser(prog="Bike Data Request", description="Request data from one device")
    parser.add_argument("device",
                        help="Select one device in this list : https://data.mobility.brussels/bike/api/counts/?request=devices&outputFormat=csv")
    parser.add_argument("start_date", help="Format : YYYYMMDD")
    parser.add_argument("end_date", help="Format : YYYYMMDD")
    args = parser.parse_args()

    df = request_device(args.device, args.start_date, args.end_date)
    path = Path(f"data/{args.device}_{args.start_date}_{args.end_date}.parquet")
    df.to_parquet(path)


if __name__ == "__main__":
    main()
