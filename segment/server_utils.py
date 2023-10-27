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

from datetime import date, timedelta

import chromedriver_autoinstaller

from webdriver_manager.chrome import ChromeDriverManager
import os
chromedriver_autoinstaller.install()



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wirewebdriver




from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
options = {
    'verify_ssl': True  # Verify SSL certificates but beware of errors with self-signed certificates
}

# Set up Chrome options
chrome_options = wirewebdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--user-data-dir=Default')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



