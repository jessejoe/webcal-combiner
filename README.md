# webcal-combiner

App to read a bunch of webcals and combine them into a single webcal that is served from a Flask endpoint. My use case was wanting a single calendar for my son's multiple concurrent basketball teams. This allows all the calendars to be combined into one that can be subscribed to by e.g. Google Calendar, iCal, etc., but still add a prefix to each event so it's obvious which team it's for. Now multiple people can all subscribe to a single calendar once, and the calendars that supply the events can be changed or updated at any time, and the combined calendar never needs to be touched.

## Usage

1. Copy `config.json.example` to `config.json`  
:warning: If the calendar starts with `webcal://` you will need to change it to `https://`
1. Edit `config.json` to add a `name` and `url` for each webcal
1. Run service: `docker-compose up -d --build`
1. Test by going to http://localhost:8080/calendar

You should see the combined calendar output starting with `BEGIN:VCALENDAR` with all the events from each calendar, prefixed with the expected `name`. Host this on a public URL and you can subscribe to it from Google Calendar, etc:

<img src="https://user-images.githubusercontent.com/1694586/233532371-a316e691-634b-4850-9a91-3b6f14b03ef6.png" width="500">

## NOTES

1. Every time the URL is polled, the calendars are re-downloaded and combined and served out, there is no caching
1. Google Calendar does not poll frequently, seems to be every ~12 hours or so, which is annoying when there's a change and you want it to show up
