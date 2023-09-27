from util import log_util as lutil, config_util
import datetime
import requests as r
import json
import re


class SignUp:
    def __init__(self, url, id, title, author, general_start_time, general_end_time):
        self.url = url
        self.id = id
        self.title = title
        self.author = author

        self.general_start_time = general_start_time
        self.general_end_time = general_end_time

        self.roles = []
        

    def to_json(self):
        roles_json_array = []
        for r in self.roles:
            roles_json_array.append(r.to_json())

        return {
                "url": self.url,
                "id": self.id,
                "title": self.title,
                "author": self.author,
                "roles": roles_json_array
            }

    def set_roles(self, roles):
        for role in roles:
            if role.start_time == 0:
                role.start_time = self.general_start_time

            if role.end_time == 0:
                role.end_time = self.general_end_time
                
        self.roles = roles


    def get_roles(self, days_out=None, days_from=0, hours_out=None, hours_from=0, include_full=True, include_ended=True):
        roles = self.roles

        if roles:
            if days_out:
                roles = [r for r in roles if r.get_days_until() <= days_out and \
                        r.get_days_until() >= days_from]
            elif hours_out:
                roles = [r for r in roles if r.get_hours_until() <= hours_out and \
                        r.get_hours_until() >= hours_from]

            if not include_full:
                roles = [r for r in roles if not r.full()]

            if not include_ended:
                roles = [r for r in roles if not r.has_ended()]

        return roles

    def get_signup_message(self,
                           days_out=None,
                           days_from=0,
                           hours_out=None,
                           hours_from=0,
                           include_full=True,
                           include_time_detail=False):
        if not days_out and not hours_out:
            return None
        
        message = ""

        roles = self.get_roles(days_out=days_out,
                               days_from=days_from,
                               hours_out=hours_out,
                               hours_from=hours_from,
                               include_full=include_full)

        full_roles_seperated = [r for r in roles if r.full()]
        roles = [r for r in roles if not r.full()]

        if roles or full_roles_seperated:
            message += "\n<hr>"
        else:
            return message
        
        when_string = ""
        if include_time_detail:
            if days_out:
                when_string = f" in the next {days_out if days_out > 1 else ''} day{'s'[:days_out^1]}"
            elif hours_out:
                when_string = f" in the next {hours_out if hours_out > 1 else ''} hour{'s'[:hours_out^1]}"

        if roles:
            whole_needed = 0
            not_full_update = []
            for r in roles:
                not_full_update.append("- " + r.get_notification_role_string())
                whole_needed += r.needed
            
            not_full_update_str = "\n".join(not_full_update)
            not_full_update_str = f"<blockquote>{not_full_update_str}</blockquote>"

            not_full_title = f"'{self.title}' has {whole_needed} slot{'s'[:whole_needed^1]}" + \
                    f" available{when_string}:"
            
            message += "\n" + not_full_title + not_full_update_str

        if full_roles_seperated:
            full_update = []
            for r in full_roles_seperated:
                full_update.append("- " + r.get_notification_role_string())
                
            full_update_str = "\n".join(full_update)
            full_update_str = f"<blockquote>{full_update_str}</blockquote>"

            full_title = f"'{self.title}' has {len(full_roles_seperated)}" + \
                    f" full volunteering role{'s'[:len(full_roles_seperated)^1]}{when_string}:"

            message += "\n" + full_title + full_update_str
        
        message += "\n" + f"Link: <a href={self.url}>{self.url}</a>" + "\n" 
        return message
        

class SignUpRole:
    def __init__(self, title, needed, start_time, end_time):
        self.title = title
        self.needed = needed
        self.start_time = start_time
        self.end_time = end_time

    def to_json(self):
        return {
                "title": self.title,
                "needed_count": self.needed,
                "start_time_string": self.start_time,
                "end_time_string": self.end_time
            }
    
    def full(self): return self.needed == 0

    def get_testing_role_string(self):
        return f"Title: {self.title}" + "\n" + \
            f"   Status: {self.needed}" + "\n" + \
            f"   Time: {self.start_time} - {self.end_time}"
   
    def get_notification_role_string(self):      
        status_string = f"{self.needed} slot{'s'[:self.needed^1]} available"
        if self.full():
            status_string = f"Full slots"

        notification_string = f"{status_string}"

        if self.start_time != 0:
            days_until = self.get_days_until()

            if days_until < 1:
                notification_string += f" <b>TODAY</b> ({self.get_time_object().strftime('%m/%d/%Y')})"
            elif days_until < 2:
                notification_string += f" <b>TOMORROW</b> ({self.get_time_object().strftime('%m/%d/%Y')})"
            else:
                notification_string += f" on {self.get_time_object().strftime('%m/%d/%Y')}"
            
            if self.end_time != 0:
                start_time_string = self.get_time_object().strftime("%-I:%M %p")
                end_time_string = self.get_end_time_object().strftime("%-I:%M %p")
                notification_string += f" from {start_time_string} to {end_time_string}"
                        
        return notification_string
    

    def get_time_object(self):
        return datetime.datetime.fromtimestamp(self.start_time)

    def get_end_time_object(self):
        return datetime.datetime.fromtimestamp(self.end_time)

    def get_hours(self):
        return (self.get_end_time_object() - self.get_time_object()).total_seconds() / 3600

    def has_ended(self):
        return datetime.datetime.now() > self.get_end_time_object()

    def get_hours_until(self):
        return ((self.get_time_object() - datetime.datetime.now()).total_seconds()) / 3600

    def get_days_until(self):
        return self.get_hours_until() / 24


BASE_SIGNUP_GENIUS_URL = "https://api.signupgenius.com/v2/k"

def fix_signupgenius_url(url):
    if "signupgenius.com" not in url:
        return None

    new_url = url.replace("://m.", "://www.").replace("/#!/showSignUp/", "/go/")
    if not new_url.endswith("#/"): new_url += "#/"
    return new_url


def get_current_signups(signup_genius_token, with_roles=True) -> [SignUp]:
    signups = []
    

    signups_json, signups_status_code = try_json_request(
        f"{BASE_SIGNUP_GENIUS_URL}/signups/created/active/",
        {"user_key": signup_genius_token}
    )

    if signups_json != None:
        signups_array = signups_json["data"]
        for signup_json in signups_array:
            signup = SignUp(
                signup_json["signupurl"],
                signup_json["signupid"],
                signup_json["title"],
                signup_json["contactname"],
                signup_json["starttime"],
                signup_json["endtime"]
            )

            signups.append(signup)

            lutil.log(f"Fetched signup '{signup.title}' with the ID '{signup.id}'")
    else:
        lutil.log(f"Unable to execute signup request. Status Code: {signups_status_code}")

    if with_roles:
        for signup in signups:
            signup.set_roles(get_signup_roles_available(signup_genius_token, signup.id))

            lutil.log(f"Set roles for signup '{signup.title}'")


    return signups

        
def get_signup_roles_available(signup_genius_token, signup_id) -> [SignUpRole]:
    roles = []
    
    params = {
        "user_key": signup_genius_token
    }

    roles_request_url = f"{BASE_SIGNUP_GENIUS_URL}/signups/report/available/{signup_id}/"

    roles_json, roles_status_code = try_json_request(roles_request_url, params)

    if roles_json != None:
        roles_array = roles_json["data"]["signup"]
        for role_json in roles_array:
            roles.append(SignUpRole(
                role_json["item"],
                role_json["myqty"], # Gives the amount of people NEEDED
                role_json["startdate"], # All the times below can be '0' (same as None)
                role_json["enddate"]
            ))
    else:
        lutil.log(f"Unable to execute roles request for signup '{signup_id}'. \
                    Status Code: '{roles_status_code}'")
    
    return roles


def try_json_request(url, params):
    current_try = 0
    found_json = None
    status_code = 0

    tries = config_util.get_config_item("request_retries")
    
    while current_try < tries:
        json_request = r.get(url, params)
        status_code = json_request.status_code

        if json_request.ok:
            try:
                found_json = json_request.json()
                lutil.log(f"Successful JSON response for URL: {url} during try {current_try}")
                break
            except json.decoder.JSONDecodeError:
                lutil.log(f"Error fetching JSON response for URL: {url} (failed at try {current_try})")

                if current_try != tries - 1:
                    lutil.log(f"Retrying JSON request for URL: {url}")
                    current_try += 1

                continue
        else:
            break


    return found_json, status_code
           
