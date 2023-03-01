import google_calendar_util as gcalutil
import signup_util as sutil
import os
import json


def file_check():
    if not os.path.exists("links.json"):
        with open("links.json", "w") as f:
            json.dump([], f)

def get_current_links():
    with open("links.json") as link_data:
        return json.load(link_data)

def update_current_links(tries):
    checked_links = []
    links = []

    for l in get_current_links():
        fixed_l = sutil.fix_signupgenius_url(l)
        if fixed_l == None or fixed_l in checked_links: continue

        signup = sutil.get_signup_data(l, tries)
        if len(signup.get_roles_not_ended()) > 0:
            links.append(fixed_l)

        checked_links.append(fixed_l)

    events = gcalutil.get_all_nhs_events()
    for e in events:
        signup_link = gcalutil.get_signup_link_from_event(e)

        if signup_link == None or signup_link in checked_links: continue

        signup = sutil.get_signup_data(signup_link, tries)
        if len(signup.get_roles_not_ended()) > 0:
            links.append(signup_link)

        checked_links.append(signup_link)

    with open("links.json", "w") as f:
        json.dump(links, f)

