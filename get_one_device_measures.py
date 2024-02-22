import pandas as pd
import requests
import datetime as dt
import sys
import argparse


def request_device(device_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """

    :param device_id:
    :type device_id:
    :param start_date:
    :type start_date:
    :param end_date:
    :type end_date:
    :return:
    :rtype:
    """
    url = f"https://data.mobility.brussels/bike/api/counts/?request=history&featureID={device_id}&startDate={start_date}&endDate={end_date}&outputFormat=json"
    response = requests.get(url)
    response.json()["data"]
    return pd.json_normalize(response.json()["data"])


def main():
    parser = argparse.ArgumentParser(prog="Bike Data Request", description="Request data from one device")
    parser.add_argument("device", help="Select one device in this list : https://data.mobility.brussels/bike/api/counts/?request=devices&outputFormat=csv")
    parser.add_argument("start_date", help="Format : YYYYMMDD")
    parser.add_argument("end_date", help="Format : YYYYMMDD")
    args = parser.parse_args()

    df = request_device(args.device, args.start_date, args.end_date)
    print(df)


if __name__ == "__main__":
    main()