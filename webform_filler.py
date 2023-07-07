#External libraries
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

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
    driver.maximize_window()
    return driver

def open_webform(driver, url):
    driver.get(url) # Open the webform

def pick_language_button_xpath(country_code):
    # Selenium uses xpath to find elements in html.
    if country_code in 45: # if country code is 45 (Denmark)
        xpath = '//input[@value="DAN"]'
    if country_code in (49, 43, 41): # if 49 = Germany, 43 = Austria, 41 = Switzerland
       xpath = '//input[@value="DEU"]'
    # else: # if country code is not 45, 49, 43 OR 41
    #     xpath = '//input[@value="ENG"]'
    print("xpath = " + xpath)
    return xpath

def click_button(driver, xpath, delay):
    try:
        element_present = expected_conditions.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, delay).until(element_present) # delays until element is present
    except TimeoutException:
       print("Timed out waiting for page to load") 
    else:
        button_to_click = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_to_click) # uses javascript to execute click. (Seleniums click function, needed to have button in view, which was problematic.)

def select_country_code_from_dropdown(driver, country_code):
    # finds dropdown element
    dropdown = driver.find_element(By.CLASS_NAME, "cc-picker") # (does not use Selenium.Select due to custom dropdown)
    # Click dropwdown to expand the options
    dropdown.click()
    # creates xpath expression to search for desired item in the dropdown
    xpath_expression= f'//span[@class="cc-picker-code" and text()="{country_code}"]'
    
    # find the desired item in the dropdown
    try:
        desired_item = driver.find_element(By.XPATH, xpath_expression)
        desired_item.click()
    except NoSuchElementException:
        print("Desired item not found in the dropdown.")
    except Exception as e:
        print(f"An error occurred while selecting the item: {e}")

def insert_number_in_text_field(driver, xpath, phone_number):
    # Find the text field for phone number and fill it with the phone number
    text_field = driver.find_element(By.XPATH, xpath)
    text_field.clear() # clear in case of previous input
    text_field.send_keys(phone_number)

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of screen

def print_report(sent_to):
    print("---\nAntal sendte spørgeskemaer: " + str(len(sent_to)) + "\nSendt til følgende telefonnumre: " + str(sent_to))
#----------------------------------------------------------------------------------------------------

# CALLS ALL FUNCTIONS ABOVE
def send_surveys(url, parsed_phone_numbers):
    driver = initialize_driver()
    open_webform(driver, url)
    delay = 5 # delay for click_buttonScripts
    sent_to_phonenumbers = []
    
    for i in parsed_phone_numbers:
        # Choose one of three languages
        language_button_xpath = pick_language_button_xpath(i[1]) # passes in second item in tuple (country code)
        click_button(driver, language_button_xpath, delay)

        #Select areacode
        select_country_code_from_dropdown(driver, i[1]) # passes in second item in tuple (country code)
        #Insert phone number
        insert_number_in_text_field(driver, '//input[@id="_Q1_O1"]', i[0]) # passes in first item in tuple (phone number)

        #Presss send
        scroll_to_bottom(driver)
        #click_button(driver, '//input[@value="Send"]', delay)
        
        #Add to sent_to list
        sent_to_phonenumbers.append(i)

        # needed for reload of page
        time.sleep(1) 
    
    # print_report(sent_to_phonenumbers)
    # driver.quit() # Quits the driver after loop is ended