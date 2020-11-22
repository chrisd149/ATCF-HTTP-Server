import csv
import os
import json

import requests
import pandas as pd

header = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure']
atcf_link = 'https://www.nrlmry.navy.mil/tcdat/sectors/atcf_sector_file'


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
            for item in header:
                csv_file_1.write(f'{item},')
            csv_file_1.write('\n')  # skip line to write data below columns

            # Writes comma delimited data to data.csv
            for row in csv_reader:
                csv_file_1.write(','.join(','.join(item.split()) for item in row) + '\n')
            e.close()
            csv_file_1.close()
            os.remove('temp.csv')  # removes temp file
            remove_last_column()  # removes empty column
        to_json()  # Copies CSV data to json
        return 200  # Good status code

    except requests.exceptions.Timeout:
        print('Timeout error occurred...')
        return 403  # Retry connection?

    except requests.HTTPError as e:
        if e == 404:
            print('HTTP error occurred...')
        return 404  # Site is down or link is bad... alert server admin


def remove_last_column():
    df = pd.read_csv('data.csv', index_col=False)
    df.drop(df.columns[9], axis=1, inplace=True)
    df.to_csv('data.csv', index=False)


def to_json():
    df = pd.read_csv('data.csv', index_col=False)
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to date if needed
    df.to_json('data.json', orient='records', indent=4)
