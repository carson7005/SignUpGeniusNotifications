from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, timedelta
import re


gc = GoogleCalendar(credentials_path="google_credentials.json")

def get_nhs_calendar():
    return gc.get_calendar(get_nhs_calendar_id())

def get_nhs_calendar_id():
    calendar_file = open("calendar_data.json")
    data = json.load(calendar_file)
    calendar_file.close()
    return data["nhs_calendar"]

def get_nhs_events():
    now = date.today()
    nhs_calendar = get_nhs_calendar_id()

    events = gc.get_events(now, calendar_id=nhs_calendar, timezone="EST")
    descriptions, filtered_events = [], []
    for e in events:
        if e.description == None: continue

        if e.description not in descriptions:
            descriptions.append(e.description)
            filtered_events.append(e)

    return filtered_events

def get_raw_description(event):
    return re.sub('<[^<]+?>', '', event.description).replace("\xa0", " ")
    
