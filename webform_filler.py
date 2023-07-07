import shutil
import openpyxl
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import PySimpleGUI as sg
import phonenumbers

def initialize_driver():
# Path to the geckodriver executable
    geckodriver_path = 'path/to/geckodriver'
    # Find the Firefox binary location using the 'shutil' module
    firefox_binary_path = shutil.which('firefox')
    # Initialize the Firefox driver using a Service object and FirefoxOptions
    service = Service(executable_path=geckodriver_path)
    firefox_options = Options()
    firefox_options.binary_location = firefox_binary_path
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def open_webform(driver, url):
    driver.get(url) # Open the webform
    #driver.maximize_window() # send-button is obscured by smaller window sizes


def get_lan_button_search_value(i):
    searchValue = ''
    if i[1] == 45: # if country code is 45 (Denmark)
        searchValue = '//input[@value="DAN"]'
    elif i[1] == 49 or 43 or 41: # if 49 = Germany, 43 = Austria, 41 = Switzerland
        searchValue = '//input[@value="DEU"]'
    elif i[1] != 45 or 49 or 43 or 41 : # if country code is not 45 (Denmark)
        searchValue = '//input[@value="ENG"]'
    return searchValue

# def ChooseLanguage():

# def DetermineAreaCode():
    
# def SelectAreaCodeFromDropdown():


def click_button(driver, xpath, delay):
    try:
        element_present = expected_conditions.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, delay).until(element_present) # delays until element is present
    except TimeoutException:
       print("Timed out waiting for page to load") 
    else:
        button_to_click = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_to_click) # uses javascript to execute click. (Seleniums click function, needed to have button in view, which was problematic.)

def fill_text_field(driver, xpath, phone_number):
    # Find the text field for phone number and fill it with the phone number
    text_field = driver.find_element(By.XPATH, xpath)
    text_field.clear()
    text_field.send_keys(phone_number)

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of screen

def print_sent_to_report(sent_to):
    print("---\nAntal sendte spørgeskemaer: " + str(len(sent_to)) + "\nSendt til følgende telefonnumre: " + str(sent_to))
#----------------------------------------------------------------------------------------------------

# CALLS ALL FUNCTIONS ABOVE
def send_surveys(url, parsed_phone_numbers):
    driver = initialize_driver()
    open_webform(driver, url)
    delay = 5 # delay for click_buttonScripts
    sent_to = []
    
    for i in parsed_phone_numbers:
        languageButtonSearchValue = get_lan_button_search_value(i)
        click_button(driver, languageButtonSearchValue, delay)
        fill_text_field(driver, '//input[@id="_Q1_O1"]', i[0]
                      )
        scroll_to_bottom(driver)
        click_button(driver, '//input[@value="Send"]', delay)
        time.sleep(1) # needed for reload of page
        sent_to.append(i)
    print_sent_to_report(sent_to)
    driver.quit() # Quits the driver after loop is ended