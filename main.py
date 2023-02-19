import signup_util as sutil
import canvas_util as cutil
import google_calendar_util as gcalutil
import argparse
from datetime import date, timedelta


def main():
    events = gcalutil.get_nhs_events()
    for e in events:
        signup = get_signup_from_event(e, 5)

        if signup == None: continue

        roles = signup.get_roles_to_notify(3)

        if not roles: continue

        print(roles)
        



def get_signup_from_event(cal_event, retries):
    desc = gcalutil.get_raw_description(cal_event).split(" ")
    for i in desc:
        url = sutil.fix_signupgenius_url(i)

        if url == None: continue

        return sutil.get_signup_data(url, retries)
    
    return None


if __name__ == "__main__":
    main()

