from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium import webdriver


class SignUp:
    def __init__(self, title, author, description, roles):
        self.title = title
        self.author = author
        self.description = description
        self.roles = roles


class SignUpRole:
    def __init__(self, title, status, location, date, start_time, end_time, full):
        self.title = title
        self.status = status
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.full = full


WHOLE_TITLE = ("h1", {"class": "signup--title-text ng-binding"})
WHOLE_AUTHOR = ("div", {"class": "pull-left signup--creator-name ng-binding"})
WHOLE_DESCRIPTION = ("p", {"class": "ng-binding", "data-ng-bind-html": "signupInfo.header.description"})

SIGNUP_CONTAINER = ("tr", {"class": "ng-scope", "data-ng-repeat": "f in filteredData | limitTo: displayLimits.dates track by f.slotid"})
SIGNUP_TITLE = ("span", {"class": "signupdata--slot-title ng-binding"})
SIGNUP_STATUS = ("span", {"class": "signup--badge ng-binding ng-scope"})

MULTI_LOCATION = ("p", {"class": "ng-binding ng-scope"})
MULTI_DATE = ("div", {"class": "signupdata--date-dt ng-binding"})
MULTI_TIMES = ("div", {"class": "signupdata--date-time ng-binding ng-scope"})

SINGLE_TIMES = ("div", {"class": "row hdr-spacer ng-scope", "data-ng-if": "showHeaderDate() && useTime && timeString != ''"})
SINGLE_DATE = ("div", {"class": "row hdr-spacer ng-scope", "data-ng-if": "showHeaderDate()"})

def get_dynamic_soup(url: str) -> BeautifulSoup:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()
        return soup


def get_dynamic_soup_seconday(url: str) -> BeautifulSoup:
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)
    driver.close()
    return soup


def get_signup_data(url: str) -> SignUp:
    soup = get_dynamic_soup(url)

    s_title = soup.find(WHOLE_TITLE[0], attrs=WHOLE_TITLE[1])
    s_author = soup.find(WHOLE_AUTHOR[0], attrs=WHOLE_AUTHOR[1])

    s_description_temp = soup.find(WHOLE_DESCRIPTION[0], attrs=WHOLE_DESCRIPTION[1])
    s_description = s_description_temp.find("p", attrs={"style": "text-align: inherit;"})

    roles = []
    containers = soup.findAll(SIGNUP_CONTAINER[0], attrs=SIGNUP_CONTAINER[1])
    
    if len(containers) == 0:
        containers = soup.findAll("tr", {"class": "ng-scope", "data-ng-repeat": "i in f.items | limitTo:displayLimit | orderBy:'itemorder'"})

    multi_signup = len(containers) > 1

    
    single_date_in = None
    single_times_in = None
    if not multi_signup:
        single_date_in = soup.find(SINGLE_DATE[0], attrs=SINGLE_DATE[1]).find("div", attrs={"class": "pull-left ng-binding"})

        single_times_temp = soup.find(SINGLE_TIMES[0], attrs=SINGLE_TIMES[1])
        single_times_in = single_times_temp.find("div", {"class": "pull-left ng-binding"}).text.split(" ")
        single_times_in.remove("-")

    for s in containers:
        role = None
        title = s.find(SIGNUP_TITLE[0], attrs=SIGNUP_TITLE[1])

        status_temp = s.find(SIGNUP_STATUS[0], attrs=SIGNUP_STATUS[1]).text
        status_array = status_temp.split(" ")
        status = None
        full = False
        if "all" in status_temp.lower():
            status = f"{status_array[1]}/{status_array[1]}"
            full = True
        elif "available" in status_temp.lower():
            status = f"0/{status_array[0]}"
        else:
            status = f"{status_array[0]}/{status_array[2]}"

        if multi_signup:
            location = s.find(MULTI_LOCATION[0], attrs=MULTI_LOCATION[1])
            date = s.find(MULTI_DATE[0], attrs=MULTI_DATE[1])

            times = s.find(MULTI_TIMES[0], attrs=MULTI_TIMES[1])
            spec_times = times.findAll("span", attrs={"class": "no-wrap"})
            start_time = spec_times[0]
            end_time = spec_times[1]

            role = SignUpRole(title.text,
                            status,
                            location.text.strip(),
                            date.text,
                            start_time.text.replace("-", ""),
                            end_time.text,
                            full)

        else:
            role = SignUpRole(title.text,
                              status,
                              None,
                              single_date_in.text.split(" ")[0],
                              single_times_in[0].lower(),
                              single_times_in[1].lower(),
                              full)

        roles.append(role)

    
    return SignUp(s_title.text, s_author.text, s_description.text, roles)
    
