"""
Description: Downloads and formats data from the ATCF sector file into a CSV file.
"""

# Python modules
import csv
from os import remove
import urllib3

# 3rd party modules
import requests

# Local modules
from ATCF_HTTPS_Server.data_processing import JsonMgr

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
                csv_file_1.write(','.join(','.join(item.split()) for item in row) + '\n')
            e.close()
            csv_file_1.close()
            remove('temp.csv')  # removes temp file
        JsonMgr.csv_to_json()  # Creates data.json
        return 200  # Good status code

    except requests.exceptions.Timeout:
        return 403  # Retry connection?

    except requests.HTTPError or urllib3.exceptions:
        return 404  # Site is down or link is bad...

