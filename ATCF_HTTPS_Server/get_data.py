import pandas as pd
import inflect

p = inflect.engine()  # Initializes inflect engine


# Returns all storms globally
def get_storms():
    df = pd.read_json('data.json')
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to date if needed
    if df.empty:
        return f'No storm data is available right now... check back later'
    else:
        return df.to_json(orient='records')


# Returns storm(s) by depression id
def get_storm_id(input_id):
    input_id = input_id.upper()
    df = pd.read_json('data.json')
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to date if needed
    new_df = df[(df['id'] == input_id)]  # row of storm data
    if new_df.empty:
        return f'{input_id} does not match any active storms'
    else:
        return new_df.to_json(orient='records')


# Returns storm(s) by name
def get_storm_name(input_name):
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
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to date if needed
    new_df = df[(df['name'] == input_name)]  # row of storm data
    if new_df.empty:
        return f'{input_name} does not match any active storms'
    else:
        return new_df.to_json(orient='records')


# Returns all storms in a basin
def get_storms_in_basin(basin):
    basin = basin.upper()
    df = pd.read_json('data.json')
    df['time'] = df['time'].astype(str).str.zfill(4)  # adds leading zeros to date if needed
    new_df = df[(df['basin'] == basin)]  # rows of storms data
    if new_df.empty:
        return f'{basin} does not match any active basins'
    else:
        return new_df.to_json(orient='records')

