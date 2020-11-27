"""
Description: Returns specified storm(s) data based on client criteria.
"""
import json

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
    return fix_all_time(data)


# Returns storm(s) by depression id
def get_storm_id(input_id: str):
    input_id = input_id.upper()
    with open('data.json') as f:
        data = json.load(f)['storms']
    for storm in data:
        storm_id = next(iter(storm))
        if storm_id == input_id:
            storm[storm_id]['time'] = storm[storm_id]['time'].zfill(4)
            return storm


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
        data = json.load(f)['storms']
    for storm in data:
        storm_id = next(iter(storm))
        if storm[storm_id]['name'] == input_name:
            storm[storm_id]['time'] = storm[storm_id]['time'].zfill(4)
            return storm


# Returns all storms in a basin
def get_storms_in_basin(basin: str):
    storms = list()
    input_basin = basin.upper()
    with open('data.json') as f:
        data = json.load(f)['storms']
    for storm in data:
        storm_id = next(iter(storm))
        if storm[storm_id]['basin'] == input_basin:
            storm[storm_id]['time'] = storm[storm_id]['time'].zfill(4)
            storms.append(storm)
    return fix_all_time(storms)


def fix_all_time(file):
    for storm in file:
        storm[next(iter(storm))]['time'] = storm[next(iter(storm))]['time'].zfill(4)
    return file



