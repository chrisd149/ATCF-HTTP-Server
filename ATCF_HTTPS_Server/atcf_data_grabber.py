"""
Description: Downloads and formats data from the ATCF sector file into a CSV file.
"""

# Python modules
import csv
from os import remove
from datetime import datetime
import urllib3
import json

# 3rd party modules
import requests
import pandas as pd
import pytz

date_now_raw = datetime.now(pytz.utc)
date_now = date_now_raw.strftime('%H:%M:%S')
csv_headers = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure', 'last-updated']

atcf_link = 'https://www.nrlmry.navy.mil/tcdat/sectors/atcf_sector_file'


# TODO: Logging
# Headers don't work, and will give out an error if used with the atcf site.
def get_atcf_data():
    # Pings atcf_link and writes information to temp.csv.  We then translate temp.csv to data.csv
    # into the proper CSV format.
    print('Pinging ATCF site...')
    try:
        # Pings ATCF link and waits 10 seconds to connect, and 15 seconds to read the data.
        response = requests.get(atcf_link, timeout=(10, 15))
        response.encoding = 'utf-8'

        # Opens temp.csv to write raw data to
        with open('temp.csv', 'w+') as b:
            b.write(response.text)
            b.close()

        # Creates data.csv where formatted data will be written to.
        csv_file_1 = open(f'data.csv', 'w+')

        # Re-open temp.csv to read the raw data, then format it and write it to data.csv.
        with open(f'temp.csv', 'r') as e:
            csv_reader = csv.reader(e, delimiter='\t')

            # Writes headers
            for item in csv_headers:
                csv_file_1.write(f'{item},')
            csv_file_1.write('\n')  # skip line to write data below columns

            # Writes comma delimited data to data.csv
            for row in csv_reader:
                csv_file_1.write(','.join(','.join(item.split()) for item in row))
                csv_file_1.write(',' + str(date_now) + '\n')
            e.close()
            csv_file_1.close()
            remove('temp.csv')  # removes temp file
        edit_csv()
        return 200  # Good status code

    except requests.exceptions.Timeout:
        edit_csv()
        return 403  # Retry connection?

    except requests.HTTPError or urllib3.exceptions:
        edit_csv()
        return 404  # Site is down or link is bad...


def edit_csv():
    # Cleans up our CSV
    df = pd.read_csv('data.csv', index_col=False)
    #df.drop(df.columns[10], axis=1, inplace=True)  # drops empty column
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to time if needed (0 -> 0000)
    df.to_csv('data.csv', index=False)
    edit_json()


def edit_json():
    df = pd.read_csv('data.csv')
    rows = len(df.index)
    raw_json = dict()
    raw_json["last-updated"] = str(date_now)
    raw_json["storms"] = []
    while rows != 0:
        rows -= 1
        row_df = df.iloc[rows, :]

        storm_data = \
            {
                f'{row_df["id"]}': [
                    {"name": f'{row_df["name"]}'},
                    {"date": f'{row_df["date"]}'},
                    {"time": f'{row_df["time"]}'},
                    {"latitude": f'{row_df["latitude"]}'},
                    {"longitude": f'{row_df["longitude"]}'},
                    {"basin": f'{row_df["basin"]}'},
                    {"vmax": f'{row_df["vmax"]}'},
                    {"pressure": f'{row_df["pressure"]}'}
                ]
            }
        raw_json["storms"].append(storm_data)
        json_data = json.dumps(raw_json, indent=4, sort_keys=True)
        print(json_data)
        with open('data.json', 'w') as outfile:
            outfile.write(json_data)

