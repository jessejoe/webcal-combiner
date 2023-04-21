# webcal-combiner

App to read a bunch of webcals and combine them into a single webcal that is served from a Flask endpoint. My use case was wanting a single calendar for my son's multiple concurrent basketball teams. This allows all the calendars to be combined into one that can be subscribed to by e.g. Google Calendar, iCal, etc., but still add a prefix to each event so it's obvious which team it's for.

## Usage

1. Copy `config.json.example` to `config.json`
1. Edit `config.json` to add a `name` and `url` for each webcal
1. Run service: `docker-compose up -d --build`
1. Test by going to http://192.168.1.11:8080/calendar

You should see the combined calendar output starting with `BEGIN:VCALENDAR` with all the events from each calendar, prefixed with the expected `name`. Host this on a public URL and you can subscribe to it from Google Calendar, etc.
