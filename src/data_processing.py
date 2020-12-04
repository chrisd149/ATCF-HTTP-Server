#!/usr/bin/env python3
# Python modules
import json
from datetime import datetime

# 3rd party modules
import pandas as pd
import pytz

from config import Config

DATA_CSV = Config.DATA_CSV
DATA_JSON = Config.DATA_JSON


class JsonMgr:
    """
    Manages json data from data.csv
    """
    def __init__(self):
        pass

    @staticmethod
    def csv_to_json(*input_arg):
        date_now_raw = datetime.now(pytz.utc)
        date_now = date_now_raw.strftime('%H:%M:%S')

        # Reads CSV as a pandas Dataframe, which we use to get all row/column information
        df = pd.read_csv(DATA_CSV)  # Reads CSV
        rows = len(df.index)  # Number of rows in CSV
        raw_json = dict()  # Empty dictionary for our JSON file

        # Adds last-updated and storms fields
        if not input_arg:
            raw_json["last-updated"] = str(date_now)  # HH:MM:SS // Current time
        else:
            # If we are calling from the JSON after it was written (after last-updated is updated.)
            # We open data.json and retrieve the last-updated field there instead of outputting the
            # current time.
            file = open(DATA_JSON, 'r')
            values = json.load(file)
            raw_json['last-updated'] = values['last-updated']  # HH:MM:SS // Current time
        raw_json["storms"] = []

        # Writes each storm data in storms list until no more rows are left to parse from the CSV.
        while rows != 0:
            # cell_data and param are None by default. If no args are passed, they stay as None objects.
            cell_data, param = None, None

            rows -= 1
            row_df = df.iloc[rows, :]  # Temp df for each row

            # If input_arg is passed, we reassign param and cell data to values in the arg (tuple),
            # and assign cell_data to the object in the Dataframe row and column of the type of
            # arg (basin, name, or id).
            if input_arg:
                param = input_arg[0]
                param_type = input_arg[1]
                if param_type == 'basin' or 'name' or 'id':
                    cell_data = (row_df[param_type])
            else:
                pass
            # Only parses and saves rows that have the cell data and params arg.  If no
            # arg is supplied, we just compare None and None (returns all data).
            if cell_data == param:
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
        if not input_arg:
            create_json(json_data)  # Create data.json (called by ATCFServer thread)
        else:
            return json_data  # Returns json_data (served to user)


def create_json(data):
    with open(DATA_JSON, 'w') as outfile:
        outfile.write(data)  # Writes json_data to data.json
