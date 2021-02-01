#!/usr/bin/env python3
"""
Description: Returns specified storm(s) data based on client criteria.
"""
# Python modules
import json

# 3rd party modules
import inflect

from src.data_processing import JsonMgr
from config import Config

DATA_JSON = Config.DATA_JSON
p = inflect.engine()  # Initializes inflect engine

csv_headers = ['id', 'name', 'date', 'time', 'latitude', 'longitude', 'basin', 'vmax', 'pressure', 'last-updated']


def check_for_storms(data: dict):
    # Checks if the requested 'storms' JSON field is empty.  If empty, the client entered
    # the wrong information, or no active storms fit the requested criteria.  NULL is passed
    # if the 'storms' field is empty.
    if len(data['storms']) == 0:
        data['storms'] = 'NULL'
        return data
    else:
        # If storms are present, correct the time values
        return fix_all_time(data)


# Returns all storms globally
def get_storms():
    with open(DATA_JSON) as f:
        data = json.load(f)
    return check_for_storms(data)


# Returns storm(s) by depression id
def get_storm_id(input_id: str):
    input_id = input_id.upper()
    data = json.loads(JsonMgr.csv_to_json(input_id, 'id'))
    return check_for_storms(data)


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

    data = json.loads(JsonMgr.csv_to_json(input_name, 'name'))
    return check_for_storms(data)


# Returns all storms in a basin
def get_storms_in_basin(basin):
    input_basin = basin.upper()
    data = json.loads(JsonMgr.csv_to_json(input_basin, 'basin'))
    return check_for_storms(data)


# Fixes all time values in a list or dictionary object
def fix_all_time(file: dict or list):
    for k in file.keys():
        if k == 'storms':
            for storm in file[k].values():
                for data in storm.values():
                    if data == 'time':
                        # Makes every time value 4 digits (i.e. 0 -> 0000, 600 -> 0600)
                        data['time'] = data['time'].zfill(4)
            return file



