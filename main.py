import signup_util as sutil
import canvas_util as cutil
import google_calendar_util as gcalutil
import argparse
from datetime import date, timedelta


def main(days_out):
    current_date_str = date.today().strftime("%m/%d/%Y")
    notif_title = f"Update for SignUps ({current_date_str})"
    notif_message = notif_title
    events = gcalutil.get_nhs_events()
    for e in events:
        signup_data = get_signup_from_event(e, 5)

        if signup_data == None: continue

        signup, url = signup_data[0], signup_data[1]

        roles = signup.get_roles_to_notify(days_out)

        if not roles: continue

        signup_string = f"'{signup.title}' needs volunteers in the next {days_out} days:"

        for r in roles:
            signup_string += "\n" + f"   {r.needed - r.current} volunteer(s) on {r.date}" + \
                    f" from {r.start_time} to {r.end_time}"

        signup_string += "\n   Url: " + url

        notif_message += "\n\n" + signup_string

    print(notif_message)
        


def get_signup_from_event(cal_event, retries):
    desc = gcalutil.get_raw_description(cal_event).split(" ")
    for i in desc:
        url = sutil.fix_signupgenius_url(i)

        if url == None: continue

        return sutil.get_signup_data(url, retries), url
    
    return None


if __name__ == "__main__":
    main(3)

