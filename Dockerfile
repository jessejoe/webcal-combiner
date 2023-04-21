FROM python:3-slim
RUN pip install requests flask ics
ADD app.py /app/app.py
ADD combine_calendars.py /app/combine_calendars.py
ADD config.json /app/config.json
CMD FLASK_APP=/app/app.py flask run --host 0.0.0.0
