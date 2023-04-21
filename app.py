"""
Serve new combined calendar
"""

import os
import json
from flask import Flask
from combine_calendars import ExistingCalendar, generate_combined_calendar

app = Flask(__name__)

cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'config.json')) as f:
    config = json.load(f)

existing_calendars = []
for calendar in config['calendars']:
    existing_calendar = ExistingCalendar(calendar['name'],
                                         calendar['description'],
                                         calendar['url'])
    existing_calendars.append(existing_calendar)


@app.route("/calendar")
def combine_calendar():
    """
    Return combined calendar in ics format
    """
    return generate_combined_calendar(config['name'], existing_calendars).serialize()
