from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response

#####################################
import json
import os
import requests
import base64
import io
from urllib.parse import urlparse
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup

import pandas as pd

from datetime import date, timedelta
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wirewebdriver
from selenium.webdriver.chrome.service import Service

# Find the login input box by its ID and enter the login credentials
from selenium.webdriver.common.by import By

service = Service((ChromeDriverManager().install()))

options = {
    "verify_ssl": True  # Verify SSL certificates but beware of errors with self-signed certificates
}

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#chrome_profile_path = "/Default"
chrome_options.add_argument("--user-data-dir=Default")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# extract artist id
def extract_artist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("artist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


# extract playlist id
def extract_playlist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("playlist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


# column name to numbers
def colnum_to_colname(colnum):
    colname = ""
    while colnum > 0:
        colnum, remainder = divmod(colnum - 1, 26)
        colname = chr(65 + remainder) + colname
    return colname


# soup from html
def soup_from_html(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    return soup


def login(driver):
    try:
        username_input = driver.find_element(By.ID, "login-username")
        username_input.send_keys("x@1111.io")
        sleep(1)
        username_input = driver.find_element(By.ID, "login-password")
        username_input.send_keys("Speedbumps123@@_121!_!3")
        sleep(1)
        driver.find_element(By.ID, "login-button").click()
        print("password entered ...")
        sleep(11)
    except:
        pass
    # Iterate over the requests made by the browser
    sleep(3)
    for request in driver.requests:
        if request.headers:
            if "authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                if auth_header != "":
                    break

    print("Authorization Header:", auth_header)

    return auth_header


def reload_auth(driver):
    driver.refresh()
    sleep(10)
    for request in driver.requests:
        if request.headers:
            if "authorization" in request.headers:
                lam = request.headers["Authorization"]
                if lam != "":
                    auth_header = lam

    print("Authorization Header:", auth_header)

    return auth_header


def get_day_of_week(date_string):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Return the day of the week
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    return days[date_obj.weekday()]

def header(auth_header):
    headers = {
        "authority": "generic.wg.spotify.com",
        "accept": "application/json",
        "accept-language": "en-US",
        "app-platform": "Browser",
        "authorization": f"{auth_header}",
        "content-type": "application/json",
        "origin": "https://artists.spotify.com",
        "referer": "https://artists.spotify.com/",
        "sec-ch-ua": '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "spotify-app-version": "1.0.0.48e3603",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "x-cloud-trace-context": "00000000000000002a87751b4619e7dc/1588903106916990606;o=1",
    }

    return headers

def extract_audience_info(row):
    total_active = int(row['active']['total'])
    super_active = int(row['active']['super'])
    moderate_active = int(row['active']['moderate'])
    light_active = int(row['active']['light'])
    programmed = int(row['programmed'])
    previously_active = int(row['previouslyActive'])

    return pd.Series([total_active, super_active, moderate_active, light_active, programmed, previously_active])



from datetime import datetime

def get_latest_date(dates):
    """
    Return the latest date from a list of date strings.

    Args:
    - dates (list of str): List of date strings in the format 'YYYY-MM-DD'.

    Returns:
    - str: Latest date string in the format 'YYYY-MM-DD'.
    """
    return max(dates, key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

