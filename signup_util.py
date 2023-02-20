from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium import webdriver
import pandas as pd
from playwright._impl._api_types import TimeoutError
import datetime


class SignUp:
    def __init__(self, url, title, author, description, roles):
        self.url = url
        self.title = title
        self.author = author
        self.description = description
        self.roles = roles

    def get_roles_to_notify(self, days_out):
        now = datetime.datetime.now()
        return [r for r in self.roles if not r.full() and \
                (r.get_time_object() - now).days <= days_out and \
                (r.get_time_object() - now).days >= 0]

    def get_roles_to_notify_hourly(self, hours_out):
        now = datetime.datetime.now()
        return [r for r in self.roles if not r.full() and \
                ((r.get_time_object() - now).total_seconds()) / 3600 <= hours_out and \
                ((r.get_time_object() - now).total_seconds()) / 3600 >= 0]



class SignUpRole:
    def __init__(self, title, current, needed, location, date, start_time, end_time):
        self.title = title
        self.current = current
        self.needed = needed
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
    
    def full(self): return self.current == self.needed

    def get_testing_role_string(self):
        return f"Title: {self.title}" + "\n" + \
            f"   Status: {self.current}/{self.needed}" + "\n" + \
            f"   Location: {self.location}" + "\n" + \
            f"   Date: {self.date}" + "\n" + \
            f"   Time: {self.start_time} - {self.end_time}"

    def get_needed_count(self):
        return self.needed - self.current

    def get_notification_role_string(self):
        role_string = ""
        count = self.get_needed_count()
        role_string += f"{count} slot{'s'[:count^1]} on {self.date}" + \
                f" from {self.start_time} to {self.end_time}"

        if self.location != None:
            role_string += f" at {self.location}"

        return role_string

    def get_time_object(self):
        return datetime.datetime.strptime(f"{self.date} {self.start_time}", "%m/%d/%Y %I:%M%p")

    def get_end_time_object(self):
        return datetime.datetime.strptime(f"{self.date} {self.end_time}", "%m/%d/%Y %I:%M%p")

    def get_hours(self):
        return (self.get_end_time_object() - self.get_time_object()).hours



class DynamicLoadError(Exception):
    def __init__(self, url, message):
        self.url = url
        self.message = message
        super().__init__(message)


WHOLE_TITLE = ("h1", {"class": "signup--title-text ng-binding"})
WHOLE_AUTHOR = ("div", {"class": "pull-left signup--creator-name ng-binding"})
WHOLE_DESCRIPTION = ("p", {"class": "ng-binding", "data-ng-bind-html": "signupInfo.header.description"})

SIGNUP_TABLE = ("table", {"class": "table table-bordered date-sorted showsegments"})


def fix_signupgenius_url(url):
    if "signupgenius.com" not in url:
        return None

    new_url = url.replace("://m.", "://www.").replace("/#!/showSignUp/", "/go/")
    if not new_url.endswith("#/"): new_url += "#/"
    return new_url


def get_dynamic_soup(url: str, retries) -> BeautifulSoup:
    current_try = 0
    soup = None
    while current_try < retries:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                soup = BeautifulSoup(page.content(), "html.parser")
                browser.close()

                if soup != None and is_valid_soup_for_signup(soup): break

                soup = None
                current_try += 1
        except TimeoutError:
            current_try += 1

    if soup == None: raise DynamicLoadError(url, f"Error while loading dynamic soup at '{url}'")
    return soup


def is_valid_soup_for_signup(soup):
    return soup.find(SIGNUP_TABLE[0], SIGNUP_TABLE[1]) != None


def get_page_data(url, retries):
    soup = get_dynamic_soup(url, retries)

    s_title = soup.find(WHOLE_TITLE[0], attrs=WHOLE_TITLE[1])
    s_author = soup.find(WHOLE_AUTHOR[0], attrs=WHOLE_AUTHOR[1])

    description = None
    s_description_temp = soup.find(WHOLE_DESCRIPTION[0], attrs=WHOLE_DESCRIPTION[1])
    if s_description_temp != None:
        s_descriptions = s_description_temp.findAll("p")
        
        descriptions = []
        if len(s_descriptions) > 0:
            for d in s_descriptions:
                descriptions.append(d.text)

            description = "\n\n".join(descriptions)

    tables = soup.find(SIGNUP_TABLE[0], SIGNUP_TABLE[1])
    if tables == None: raise DynamicLoadError(url, f"Table for signup at '{url}' is null")
    data = pd.read_html(tables.prettify(), displayed_only=False)

    table = data[0]
    
    slot_label = "Available Slot"
    if slot_label not in table.columns:
        slot_label = "Volunteer"
    for i in range(len(table[slot_label])):
        s = table[slot_label][i]
        if(str(s) == "nan"): table = table.drop(i)

    table = table.reset_index()
    table = table.drop(columns=["index"])
    return {
            "table": table,
            "title": s_title.text,
            "author": s_author.text,
            "description": description
        }


def get_signup_data(url: str, retries):
    data = get_page_data(url, retries)

    table = data["table"]

    roles = []
    for i in range(len(table.index)):
        row = table.loc[i]

        date = str(row["Date"]).split("  ")[0]

        location = str(row["Location"]).split("  ")[0]
        if str(location) == "nan":
            location = None

        full_time = str(row["Time"]).split("  ")
        start_time = full_time[0].replace("-", "")
        end_time = full_time[1]

        slot_label = "Available Slot"
        if slot_label not in row:
            slot_label = "Volunteer"

        slot_array = str(row[slot_label]).split("  ")
                
        title = slot_array[1]
        
        current = 0
        needed = 0
        status = slot_array[2].split(" ")
        if status[0] == "All":
            current = int(status[1])
            needed = current
        elif status[1] == "slots":
            needed = int(status[0])
        else:
            current = int(status[0])
            needed = int(status[2])

        roles.append(SignUpRole(title, current, needed, location, date, start_time, end_time))

    return SignUp(url, data["title"], data["author"], data["description"], roles)

