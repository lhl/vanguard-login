#!/usr/bin/python


import json
import os
import selenium
from   selenium import webdriver
from   selenium.webdriver.common.by import By
from   selenium.webdriver.support.ui import WebDriverWait
from   selenium.webdriver.support import expected_conditions as EC
import sys
import time


### Login Credentials
# You might want to load via ENV or secure keystore etc, can be dangerous to have 
# sitting on your drive
creds = json.load(open('vanguard.creds'))
LOGIN = creds['login']
PASSWORD = creds['password']


### Browser Setup - Using Chrome in headless mode
# alternative: https://www.alexkras.com/running-chrome-and-other-browsers-in-almost-headless-mode/
CHROMEDRIVER = '/usr/bin/chromedriver'
options = webdriver.ChromeOptions()

# Specify your preferred version of Chrome
options.binary_location = '/usr/bin/chromium' 

# Default Headless Options - can comment out if you want to see it on screen
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=600,800")

# If you want to specify a particular home folder (otherwise will use temp)
# https://chromium.googlesource.com/chromium/src/+/master/docs/user_data_dir.md#Linux
options.add_argument('--user-data-dir={}/.config/chromium'.format(os.environ['HOME']))

# If you want to test the full process this is useful
# options.add_argument('--incognito')

service_args = []
service_log_path = './chromedriver.log'

# DEBUG - lots of info
# service_args = ['--verbose']

browser = webdriver.Chrome(CHROMEDRIVER,
                           chrome_options=options,
                           service_args=service_args,
                           service_log_path=service_log_path)


### Login
LOGIN_URL = 'https://investor.vanguard.com/home/'
browser.get(LOGIN_URL)
username = browser.find_element_by_id('USER')
password = browser.find_element_by_id('PASSWORD')
username.send_keys(LOGIN)
password.send_keys(PASSWORD)
browser.find_element_by_id('login').click()

### 1st Time Browser Auth
if browser.current_url.startswith('https://personal.vanguard.com/us/AuthLogin'):
  # Maybe there's a more robust way to do this...
  question = browser.find_elements_by_xpath('//form[@id="LoginForm"]//tr[2]/td[2]')[0].text
  ANSWER = input('{}: '.format(question))
  answer = browser.find_element_by_id('LoginForm:ANSWER')
  browser.find_element_by_id('labeloption1').click()
  browser.find_element_by_id('LoginForm:ContinueInput').click()


### Summary
'''
we might want to check cookies to see if we're succesfully logged in:
 (double-check url, will be redirected otherwise)
'''
# https://personal.vanguard.com/my-accounts/account-overview/balances
print(browser.current_url)
browser.save_screenshot("summary.png")

### Quit
browser.quit()
