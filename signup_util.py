import pandas as pd
import datetime
import page_util as putil
import log_util as lutil


class SignUp:
    def __init__(self, url, title, author, description, roles):
        self.url = url
        self.title = title
        self.author = author
        self.description = description
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
        
        status_string = f"{count if count > 0 else 'No'} slot{'s'[:count^1]} available"

        role_string += f"{status_string} on {self.date}" + \
                f" from {self.start_time} to {self.end_time}"

        if self.location != None:
            role_string += f" at {self.location}"

        return role_string

    def get_time_object(self):
        return datetime.datetime.strptime(f"{self.date} {self.start_time}", "%m/%d/%Y %I:%M%p")

    def get_end_time_object(self):
        return datetime.datetime.strptime(f"{self.date} {self.end_time}", "%m/%d/%Y %I:%M%p")

    def get_hours(self):
        return (self.get_end_time_object() - self.get_time_object()).total_seconds() / 3600

    def has_ended(self):
        return datetime.datetime.now() > self.get_end_time_object()

    def get_hours_until(self):
        return ((self.get_time_object() - datetime.datetime.now()).total_seconds()) / 3600

    def get_days_until(self):
        return self.get_hours_until() / 24



WHOLE_TITLE = ("h1", {"class": "signup--title-text ng-binding"})
WHOLE_AUTHOR = ("div", {"class": "pull-left signup--creator-name ng-binding"})
WHOLE_DESCRIPTION = ("p", {"class": "ng-binding", "data-ng-bind-html": "signupInfo.header.description"})

SIGNUP_TABLE_CONTAINER = ("div", {"class": "row data-grid ng-scope"})

SIGNUP_EXTRA_DETAILS = ("div", {"class": "row hdr-spacer ng-scope"})


def fix_signupgenius_url(url):
    if "signupgenius.com" not in url:
        return None

    new_url = url.replace("://m.", "://www.").replace("/#!/showSignUp/", "/go/")
    if not new_url.endswith("#/"): new_url += "#/"
    return new_url



def get_signup_table(soup):
    table_container = soup.find(SIGNUP_TABLE_CONTAINER[0], SIGNUP_TABLE_CONTAINER[1])
    if table_container == None:
        return None

    return table_container.find("table")


def get_page_data(url, retries, browser_instance=None):
    lutil.log(f"Getting Data for {url}")
    soup = putil.get_selenium_soup(url, retries, browser_instance)

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

    tables = get_signup_table(soup)
    if tables == None: raise DynamicLoadError(url, f"Table for signup at '{url}' is null")
    data = pd.read_html(tables.prettify(), displayed_only=False)

    table = data[0]
    print(table.columns)
    
    slot_label_i = len(table.columns) - 1
    slot_label = table.columns[slot_label_i]
    while "Unnamed" in slot_label:
        slot_label_i -= 1
        slot_label = table.columns[slot_label_i]

    print(f"Slot Label: {slot_label}")
    for i in range(len(table[slot_label])):
        s = table[slot_label][i]
        if(str(s) == "nan"): table = table.drop(i)

    table = table.reset_index()
    table = table.drop(columns=["index"])

    page_data_object = {
            "table": table,
            "title": s_title.text,
            "author": s_author.text,
            "description": description,
            "slot_label": slot_label
        }


    extra_data = list(soup.findAll(SIGNUP_EXTRA_DETAILS[0], SIGNUP_EXTRA_DETAILS[1]))
    DETAIL_TITLE_ATT = ("strong", {"class": "ng-binding"})
    extra_data = [d for d in extra_data if d.find(DETAIL_TITLE_ATT[0], DETAIL_TITLE_ATT[1]).text != "Share"]
    if len(extra_data) > 0:
        for d in extra_data:
            detail_title = d.find(DETAIL_TITLE_ATT[0], DETAIL_TITLE_ATT[1]).text
            DETAIL_TEXT_ATT = ("div", {"class": "pull-left ng-binding"})
            match detail_title:
                case "Date":
                    detail_text = d.find(DETAIL_TEXT_ATT[0], DETAIL_TEXT_ATT[1]).text
                    page_data_object["whole_date"] = detail_text.split(" ")[0]
                case "Time":
                    detail_text = d.find(DETAIL_TEXT_ATT[0], DETAIL_TEXT_ATT[1]).text
                    time_array = detail_text.split(" ")
                    page_data_object["whole_start_time"] = time_array[0]
                    page_data_object["whole_end_time"] = time_array[2]
                case "Location":
                    detail_text = d.find("span", {"class": "ng-binding"}).text
                    page_data_object["whole_location"] = detail_text

    return page_data_object


def get_signup_data(url: str, retries, browser_instance=None):
    data = get_page_data(url, retries, browser_instance)

    table = data["table"]
    print(table)

    roles = []

    for i in range(len(table.index)):
        row = table.loc[i]

        
        date = None
        if "Date" in row:
            date = str(row["Date"]).split("  ")[0]
        elif "whole_date" in data:
            date = data["whole_date"]
        
        location = None
        if "Location" in row:
            location = str(row["Location"]).split("  ")[0]
            if str(location) == "nan":
                location = None
        elif "whole_location" in data:
            location = data["whole_location"]
        
        start_time = None
        end_time = None
        if "Time" in row:
            full_time = str(row["Time"]).split("  ")
            start_time = full_time[0].replace("-", "")
            end_time = full_time[1]
        elif "whole_start_time" in data and "whole_end_time" in data:
            start_time = data["whole_start_time"]
            end_time = data["whole_end_time"]

        slot_label = data["slot_label"]
        slot_array = str(row[slot_label]).split("  ")
        if len(slot_array) <= 1: continue
                
        title = slot_array[1]
        title_check = title.split(" ")[0]
        title_correction = 0
        if title_check == "Full" or title_check == "All" or \
                title_check.isnumeric():
                    title_correction = 1
                    title = None
        
        current = 0
        needed = 0
        status = slot_array[2 - title_correction].split(" ")
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

