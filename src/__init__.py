# Python modules
from datetime import datetime, timedelta
from time import sleep

# 3rd party modules
from flask import Flask, request, jsonify, render_template
import pytz

# Local modules
from src import atcf_data_grabber, get_data
from config import DevelopmentConfig


class ATCFServer:
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
            date_now_raw = datetime.now(pytz.utc)
            date_now = date_now_raw.strftime('%H:%M:%S')
            if code == 403:
                if tries >= 5:  # We returned code 403 five or more times in a row
                    print('Site is down, we will ping later...')
                    tries = 0
                    self.sleep()
                    continue
                print('Timeout connection... retrying...')
                tries += 1
                sleep(5)
                continue
            if code == 404:
                print('Site is down, we will ping later...')
                self.sleep()
                continue
            if code == 200:
                tries = 0  # resets tries
                print(f'Successfully downloaded ATCF data at {date_now}')
                self.sleep()

    @staticmethod
    def next_interval():
        round_mins = 15
        now = datetime.now()
        mins = now.minute - (now.minute % round_mins)
        next_interval = datetime(now.year, now.month, now.day, now.hour, mins) + timedelta(minutes=round_mins)
        return next_interval, now

    def sleep(self):
        func = self.next_interval()
        interval, now = func[0], func[1]
        seconds_to_sleep = interval - now
        if seconds_to_sleep.total_seconds() <= 15:
            # Prevents sleeping a negative amount (bad) since we subtract a few seconds when
            # doing an extended sleep.
            sleep(5)
        else:
            sleep(seconds_to_sleep.total_seconds() - 10)


app = Flask(__name__)
config = DevelopmentConfig


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# Default GET response, returns all formatted data
@app.route('/api/', methods=['GET'])
def get_all():
    return jsonify(get_data.get_storms())


# Returns specific storms based on depression id (i.e. 23L), name (i.e. POLO) or basin (i.e IO).
# Must add "/args/?" + "name=NAME" or "id=ID" to end of server ip.
@app.route('/api/args', methods=['GET'])
def args():
    # Possible args (id or name)
    id = request.args.get('id')  # depression id
    name = request.args.get('name')  # storm name
    basin = request.args.get('basin')

    if not id or not name:
        pass  # if no id or name or basin is passed we skip it
    if id:
        return jsonify(get_data.get_storm_id(id))
    if name:
        return jsonify(get_data.get_storm_name(name))
    if basin:
        return jsonify(get_data.get_storms_in_basin(basin))
