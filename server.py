# Python modules
from datetime import datetime
from threading import Thread
import time

# 3rd party modules
from flask import Flask, Response, request

# Local modules
from ATCF_HTTPS_Server import atcf_data_grabber, get_data


date_now = datetime.now()


# TODO: Add logging
class Server:
    # Downloads data from the ATCF site on a set interval.
    # Based on the code returned by get_atcf_data(), we can
    # try to continue the program or reconnect with the ATCF
    # site.
    def __init__(self):
        tries = 0
        while True:
            # Possible codes:
            # 200 -> Good
            # 403 -> Timeout Error
            # 404 -> HTTPError (bad)
            code = atcf_data_grabber.get_atcf_data()  # Code returned by the function
            if code == 403:
                if tries >= 5:  # We returned code 403 five or more times in a row
                    print('Site is down, we will ping later...')
                    tries = 0
                    time.sleep(890)
                    continue
                print('Timeout connection... retrying...')
                tries += 1
                continue
            if code == 404:
                print('Site is down, we will ping later...')
                time.sleep(890)
                # TODO: Ping the devs
                continue
            if code == 200:
                tries = 0  # resets tries
                print(f'Successfully downloaded ATCF data at {date_now}')
                time.sleep(890)


app = Flask(__name__)


# Default GET response, returns all formatted data
@app.route('/', methods=['GET'])
def get_all():
    return Response(get_data.get_storms(), mimetype='application/json')


# Returns specific storms based on depression id (i.e. 23L), name (i.e. POLO) or basin (i.e IO).
# Must add "/args/?" + "name=NAME" or "id=ID" to end of server ip.
@app.route('/args/', methods=['GET'])
def args():
    # Possible args (id or name)
    id = request.args.get('id')  # depression id
    name = request.args.get('name')  # storm name
    basin = request.args.get('basin')

    if not id or not name:
        pass  # if no id or name or basin is passed we skip it
    if id:
        return Response(get_data.get_storm_id(id), mimetype='application/json')
    if name:
        return Response(get_data.get_storm_name(name), mimetype='application/json')
    if basin:
        return Response(get_data.get_storms_in_basin(basin), mimetype='application/json')


if __name__ == "__main__":
    Thread(target=Server).start()  # Read class description
    Thread(app.run(host="127.0.0.1", debug=False)).start()  # Flask server






