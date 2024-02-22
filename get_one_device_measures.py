import pandas as pd
import requests
import datetime as dt
import sys


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
    device = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    df = request_device(device, start_date, end_date)
    print(df)


if __name__ == "__main__":
    main()