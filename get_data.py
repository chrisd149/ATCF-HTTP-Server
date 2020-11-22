import pandas as pd


def get_storms():
    df = pd.read_json('data.json')
    return df.to_json(orient='records')


def get_storm_id(input_id):
    df = pd.read_json('data.json')
    new_df = df[(df['id'] == input_id)]
    return new_df.to_json(orient='records')


def get_storm_name(input_name):
    df = pd.read_json('data.json')
    new_df = df[(df['name'] == input_name)]
    return new_df.to_json(orient='records')


def get_storms_in_basin(basin):
    df = pd.read_json('data.json')
    new_df = df[(df['basin'] == basin)]
    return new_df.to_json(orient='records')

