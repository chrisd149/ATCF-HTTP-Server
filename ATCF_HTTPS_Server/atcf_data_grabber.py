# Python modules
import csv
import os
# 3rd party modules
import requests
import pandas as pd

csv_headers = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure']
http_headers = {"User-Agent":
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

atcf_link = 'https://www.nrlmry.navy.mil/tcdat/sectors/atcf_sector_file'


# TODO: Logging
def get_atcf_data():
    # Pings atcf_link and writes information to temp.csv.  We then translate temp.csv to data.csv
    # into the proper CSV format.
    print('Pinging ATCF site...')
    try:
        # Pings ATCF link and waits 10 seconds to connect, and 15 seconds to read the data.
        response = requests.get(atcf_link, headers=http_headers, timeout=(10, 15))
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
                csv_file_1.write(','.join(','.join(item.split()) for item in row) + '\n')
            e.close()
            csv_file_1.close()
            os.remove('temp.csv')  # removes temp file
        edit_csv()
        return 200  # Good status code

    except requests.exceptions.Timeout:
        return 403  # Retry connection?

    except requests.HTTPError:
        return 404  # Site is down or link is bad...


def edit_csv():
    # Cleans up our CSV
    df = pd.read_csv('data.csv', index_col=False)
    df.drop(df.columns[9], axis=1, inplace=True)  # column 9 is empty
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to time if needed (0 -> 0000)
    df.to_csv('data.csv', index=False)
