"""
Class and function for combining existing ics calendars
"""
import logging
from dataclasses import dataclass
from ics import Calendar
from ics.grammar.parse import ContentLine
import requests


@dataclass
class ExistingCalendar:
    """
    Dataclass to represent an existing calendar
    """
    name: str
    description: str
    url: str


def generate_combined_calendar(name: str, calendars: list):
    """
    Generate a new calendar with events from the exsting calendars

    :param name: Name of new calendar
    :param calendars: List of `ExistingCalendar()` objects
    :return: New `ics.Calendar()`
    """
    new_cal = Calendar()
    new_cal.extra.append(ContentLine(name="NAME", value=name))
    new_cal.extra.append(ContentLine(name="X-WR-CALNAME", value=name))
    # Attempt to tell client to refresh after 1 hour, this may not be widely adopted or
    # honored - https://www.rfc-editor.org/rfc/rfc7986.html#page-9
    new_cal.extra.append(ContentLine(name="REFRESH-INTERVAL;VALUE=DURATION", value='PT1H'))

    for calendar in calendars:
        resp = requests.get(calendar.url, timeout=30)
        resp.raise_for_status()

        calendar_obj = Calendar(resp.text)
        for event in calendar_obj.events:
            # Prepend calendar name to event name to make calendars easier to identify
            if calendar.name:
                event.name = f'[{calendar.name}] {event.name}'
            logging.info('New event name: %s', event.name)

            # 'X-APPLE-STRUCTURED-LOCATION' is used by band.us webcals and breaks Google Calendar, even though it works
            # fine with the band.us calendar directly ¯\_(ツ)_/¯
            bad_fields = ['X-APPLE-STRUCTURED-LOCATION']
            bad_field_objs = [item for item in event.extra if item.name in bad_fields]
            for bad_field_obj in bad_field_objs:
                logging.info(f'Removing field {bad_field_obj.name} from {event.name}')
                event.extra.remove(bad_field_obj)

            new_cal.events.add(event)

    return new_cal
