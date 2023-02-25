from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError
import signup_util as sutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class DynamicLoadError(Exception):
    def __init__(self, url, message):
        self.url = url
        self.message = message
        super().__init__(message)


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

                if soup != None and sutil.get_signup_table(soup) != None: break

                soup = None
                current_try += 1
        except TimeoutError:
            current_try += 1

    if soup == None: raise DynamicLoadError(url, f"Error while loading dynamic soup at '{url}'")
    return soup


def get_selenium_soup(url: str, tries, browser_instance=None):
    current_try = 0
    soup = None
    browser = None
    while current_try < tries:
        if not browser_instance:
            ff_options = Options()
            ff_options.headless = True
            print("Opening Browser...")
            browser = webdriver.Firefox(options=ff_options)
        else:
            browser = browser_instance
        print("Getting URL...")
        browser.get(url)
        print("Sleeping...")
        time.sleep(3)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if soup != None and sutil.get_signup_table(soup) != None: break
        
        soup = None
        current_try += 1

    if not browser_instance:
        browser.close()
    
    if soup == None: raise DynamicLoadError(url, f"Error while loading dynamic soup at '{url}'")
    return soup

