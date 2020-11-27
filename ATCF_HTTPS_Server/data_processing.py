import json
from datetime import datetime

import pandas as pd
import pytz

date_now_raw = datetime.now(pytz.utc)
date_now = date_now_raw.strftime('%H:%M:%S')


def edit_csv():
    # Cleans up our CSV
    df = pd.read_csv('data.csv', index_col=False)
    df.drop(df.columns[9], axis=1, inplace=True)  # drops empty column
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
        raw_json["storms"].append(storm_data)
    json_data = json.dumps(raw_json, indent=4, sort_keys=True)
    with open('data.json', 'w') as outfile:
        outfile.write(json_data)
