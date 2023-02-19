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
        
        whole_count = 0
        signup_string = ""

        for r in roles:
            count = r.needed - r.current
            signup_string += "\n" + f"   {count} slot{'s'[:count^1]} on {r.date}" + \
                    f" from {r.start_time} to {r.end_time}"

            if r.location != None:
                signup_string += f" at {r.location}"

            whole_count += count

        signup_string += "\n" + f"   Url: <a href={url}>{url}</a>"

        signup_string = f"'{signup.title}' has {whole_count} volunteering" + \
                f" slot{'s'[:whole_count^1]} available in the next {days_out} days:" + \
                signup_string


        notif_message += "\n\n" + signup_string

    print(notif_message)
    cutil.send_announcement(6768, notif_title, notif_message.replace("\n", "<br>"))        


def get_signup_from_event(cal_event, retries):
    desc = gcalutil.get_raw_description(cal_event).split(" ")
    for i in desc:
        url = sutil.fix_signupgenius_url(i)

        if url == None: continue

        return sutil.get_signup_data(url, retries), url
    
    return None


if __name__ == "__main__":
    main(3)

