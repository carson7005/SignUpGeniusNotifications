from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import argparse

class SignUp:
    def __init__(self, title, status, location, date, day, startTime, endTime):
        self.title = title
        self.status = status
        self.location = location
        self.date = date
        self.day = day
        self.startTime = startTime
        self.endTime = endTime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("signup")
    args = parser.parse_args()

    if not args.signup:
        print("No SignUp Specified")
        return
    else:
        print("Thinking...")


    def get_dynamic_soup(url: str) -> BeautifulSoup:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            soup = BeautifulSoup(page.content(), "html.parser")
            browser.close()
            return soup
    
    SIGNUP_CONTAINER = ("tr", {"class": "ng-scope", "data-ng-repeat": "f in filteredData | limitTo: displayLimits.dates track by f.slotid"})
    SIGNUP_TITLE = ("span", {"class": "signupdata--slot-title ng-binding"})
    SIGNUP_STATUS = ("span", {"class": "signup--badge ng-binding ng-scope"})
    SIGNUP_LOCATION = ("p", {"class": "ng-binding ng-scope"})
    SIGNUP_DATE = ("div", {"class": "signupdata--date-dt ng-binding"})
    SIGNUP_TIMES = ("div", {"class": "signupdata--date-time ng-binding ng-scope"})
    SIGNUP_DAY = ("div", {"class": "signupdata--date-day ng-binding"})

    signups = []

    soup = get_dynamic_soup(args.signup)
    containers = soup.findAll(SIGNUP_CONTAINER[0], attrs=SIGNUP_CONTAINER[1])

    print("Current Sign Up Status: ")
    for s in containers:
        title = s.find(SIGNUP_TITLE[0], attrs=SIGNUP_TITLE[1])
        status = s.find(SIGNUP_STATUS[0], attrs=SIGNUP_STATUS[1])
        location = s.find(SIGNUP_LOCATION[0], attrs=SIGNUP_LOCATION[1])
        date = s.find(SIGNUP_DATE[0], attrs=SIGNUP_DATE[1])
        day = s.find(SIGNUP_DAY[0], attrs=SIGNUP_DAY[1])

        times = s.find(SIGNUP_TIMES[0], attrs=SIGNUP_TIMES[1])
        specTimes = times.findAll("span", attrs={"class": "no-wrap"})
        startTime = specTimes[0]
        endTime = specTimes[1]

        signup = SignUp(title.text,
                        status.text,
                        location.text.strip(),
                        date.text,
                        day.text,
                        startTime.text,
                        endTime.text)

        signups.append(signup)
    
    for signup in signups:
        print(f"{signup.title}:" + "\n" +
              f"   Status: {signup.status}" + "\n" +
              f"   Location: {signup.location}" + "\n" +
              f"   Date: {signup.date}" + "\n" +
              f"   Day: {signup.day}" + "\n" +
              f"   Start Time: {signup.startTime}" + "\n" +
              f"   End Time: {signup.endTime}" + "\n\n" +
              "--------------------------------------------\n")


if __name__ == "__main__":
    main()
