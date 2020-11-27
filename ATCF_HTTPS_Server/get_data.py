"""
Description: Returns specified storm(s) data based on client criteria.
"""
import json

import pandas as pd
import inflect

p = inflect.engine()  # Initializes inflect engine

csv_headers = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure', 'last-updated']
# For all functions, we check if the requested Dataframe (df) is empty.  If so, either
# the client entered the wrong information, or no active storms fit the requested
# criteria.


# Returns all storms globally
def get_storms():
    with open('data.json') as f:
        data = json.load(f)['storms']
    for storm in data:
        storm[next(iter(storm))]['time'] = storm[next(iter(storm))]['time'].zfill(4)
    return data


# Returns storm(s) by depression id
def get_storm_id(input_id: str):
    input_id = input_id.upper()
    df = pd.read_json('data.json')
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to time if needed
    new_df = df[(df['id'] == input_id)]  # row of storm data
    if new_df.empty:
        return f'{input_id} does not match any active storms'
    else:
        return new_df.to_json(orient='records')


# Returns storm(s) by name
def get_storm_name(input_name: str or int):
    # Only accepts strings, however we can convert numbers to word form if possible, as depressions
    # are named with a number (i.e FOUR).

    # Tries to convert input name to int.  If no value error is risen, input_name is converted
    # to word form (i.e. 4 -> four).
    try:  # Input name is an int, convert to word form
        int(input_name)
        input_name = p.number_to_words(input_name).upper()
    except ValueError:  # Input name is already a string/not an int
        input_name = input_name.upper()

    df = pd.read_json('data.json')
    new_df = df[(df['name'] == input_name)]  # row of storm data
    if new_df.empty:
        return f'{input_name} does not match any active storms'
    else:
        return new_df.to_json(orient='records')


# Returns all storms in a basin
def get_storms_in_basin(basin: str):
    basin = basin.upper()
    df = pd.read_json('data.json')
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to time if needed
    new_df = df[(df['basin'] == basin)]  # rows of storms data
    if new_df.empty:
        return f'{basin} does not match any active basins'
    else:
        return new_df.to_json(orient='records')





