"""
Creates our data.json file based on the data in data.csv.
"""

# Python modules
import json
from datetime import datetime

# 3rd party modules
import pandas as pd
import pytz

date_now_raw = datetime.now(pytz.utc)
date_now = date_now_raw.strftime('%H:%M:%S')


class JsonMgr:
    """
    Manages json data from data.csv
    """
    def __init__(self):
        pass

    @staticmethod
    def csv_to_json(*input_basin):
        # Reads CSV as a pandas Dataframe, which we use to get all row/column information
        df = pd.read_csv('data.csv')  # Reads CSV
        rows = len(df.index)  # Number of rows in CSV
        raw_json = dict()  # Empty dictionary for our JSON file

        # Adds last-updated and storms fields
        raw_json["last-updated"] = str(date_now)  # HH:MM:SS
        raw_json["storms"] = []

        # Writes each storm data in storms list until no more rows are left to parse from the CSV.
        while rows != 0:
            rows -= 1
            row_df = df.iloc[rows, :]  # Temp df for each row
            # If input_basin arg isn't passed, we make it equal whatever is the basin found in the row.
            # basin will equal input_basin if passed, however will equal the basin found in the row
            # if no input_basin arg is passed. (No arg passed = we want every storm regardless of basin.)
            if not input_basin:
                basin = (row_df["basin"],)
            else:
                basin = input_basin
            # Only parses and saves rows that have the basin that equals the basin arg.  If no
            # arg is supplied, we use the basin found in the row as the arg.
            if row_df["basin"] == basin[0]:
                # JSON data
                storm_data = \
                    {
                        f'{row_df["id"]}': {
                            "name": f'{row_df["name"]}',
                            "date": f'{row_df["date"]}',
                            "time": f'{row_df["time"]}',
                            "latitude": f'{row_df["latitude"]}',
                            "longitude": f'{row_df["longitude"]}',
                            "basin": f'{row_df["basin"]}',
                            "vmax": f'{row_df["vmax"]}',
                            "pressure": f'{row_df["pressure"]}'
                        }
                    }
                raw_json["storms"].append(storm_data)  # Appends storm_data dict to storms list
        # Converts raw_json dictionary to JSON
        json_data = json.dumps(raw_json, indent=4, sort_keys=True)
        if not input_basin:
            create_json(json_data)  # Create data.json (called by ATCFServer thread)
        else:
            return json_data  # Returns json_data (served to user)


def create_json(data):
    with open('data.json', 'w') as outfile:
        outfile.write(data)  # Writes json_data to data.json
