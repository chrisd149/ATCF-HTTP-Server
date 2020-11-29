"""
Description: Returns specified storm(s) data based on client criteria.
"""
# Python modules
import json

# 3rd party modules
import inflect

from ATCF_HTTPS_Server.data_processing import JsonMgr

p = inflect.engine()  # Initializes inflect engine

csv_headers = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure', 'last-updated']

# For all functions, we check if the requested Dataframe (df) is empty.  If so, either
# the client entered the wrong information, or no active storms fit the requested
# criteria.


# Returns all storms globally
def get_storms():
    with open('data.json') as f:
        data = json.load(f)
    return fix_all_time(data)


# Returns storm(s) by depression id
def get_storm_id(input_id: str):
    input_id = input_id.upper()
    with open('data.json') as f:
        data = json.load(f)
    # For every storm stored, we check if it's id matches the user id.
    for storm in data['storms']:
        storm_id = next(iter(storm))  # Stores dictionary key as our storm id
        if storm_id == input_id:
            storm[storm_id]['time'] = storm[storm_id]['time'].zfill(4)  # Fixes leading zeros
            return storm  # Returns specified storm


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

    with open('data.json') as f:
        data = json.load(f)
    # For every storm stored, we check if it's name matches the user name.
    for storm in data['storms']:
        storm_id = next(iter(storm))  # Stores dictionary key for indexing
        if storm[storm_id]['name'] == input_name:
            storm[storm_id]['time'] = storm[storm_id]['time'].zfill(4)  # Fixes leading zeros
            return storm


# Returns all storms in a basin
def get_storms_in_basin(basin):
    input_basin = basin.upper()
    return json.loads(JsonMgr.csv_to_json(input_basin))


# Fixes all time values in a list or dictionary object
def fix_all_time(file: dict or list):
    for storm in file['storms']:
        # Makes every time value 4 digits (i.e. 0 -> 0000, 600 -> 0600)
        storm[next(iter(storm))]['time'] = storm[next(iter(storm))]['time'].zfill(4)
    return file



