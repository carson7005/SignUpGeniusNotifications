from gcsa.google_calendar import GoogleCalendar
import json
import datetime

gc = GoogleCalendar(credentials_path="google_credentials.json")

def get_nhs_calendar():
    calendar_file = open("calendar_data.json")
    data = json.load(calendar_file)
    calendar_file.close()

    return gc.get_calendar(data["nhs_calendar"])


def get_nhs_events(days_from, days_to):
    now = datetime.datetime.now()
    d_from = now + datetime.timedelta(days=days_from)
    d_to = now + datetime.timedelta(days=days_to)
    nhs_calendar = get_nhs_calendar()
    return gc.get_events(d_from, d_to, calendar_id=nhs_calendar.id)
    
