from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, timedelta
import re
import signup_util as sutil


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


def get_all_nhs_events():
    nhs_calendar = get_nhs_calendar_id()

    events = gc.get_events(calendar_id=nhs_calendar, timezone="EST")
    descriptions, filtered_events = [], []
    for e in events:
        if e.description == None: continue

        if e.description not in descriptions:
            descriptions.append(e.description)
            filtered_events.append(e)

    return filtered_events


def get_raw_description(event):
    return re.sub('<[^<]+?>', '', event.description).replace("\xa0", " ")


def get_signup_link_from_event(cal_event):
    desc = get_raw_description(cal_event).split(" ")
    for i in desc:
        url = sutil.fix_signupgenius_url(i)

        if url != None: return url

    return None
    

def get_signup_from_event(cal_event, retries):
    url = get_signup_link_from_event(cal_event, retries)

    if url == None: return None

    return sutil.get_signup_data(url, retries)

