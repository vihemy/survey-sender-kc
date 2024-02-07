import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from phonenumber_class import PhoneNumber
import printer

# Constants for configuration and xpaths
GECKODRIVER_PATH = "path/to/geckodriver"
BUTTON_CLICK_TIMEOUT = 5  # Timeout in seconds
LANGUAGE_BUTTON_XPATH = '//input[@value="{lang}"]'
COUNTRY_DROPDOWN_XPATH = "//div[@class='cc-picker cc-picker-code-select-enabled']"
COUNTRY_CODE_XPATH = '//span[@class="cc-picker-code" and text()="{code}"]'
PHONE_FIELD_XPATH = '//input[@id="_Q1_O1"]'
SEND_BUTTON_XPATH = '//input[@value="Send"]'
FIREFOX_BINARY_PATH = shutil.which("firefox")


def initialize_driver():
    service = Service(executable_path=GECKODRIVER_PATH)
    firefox_options = Options()
    firefox_options.binary_location = FIREFOX_BINARY_PATH
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.maximize_window()
    return driver


def navigate_to_url(driver, url):
    driver.get(url)


def pick_language_button_xpath(phone_number: PhoneNumber):
    lang = phone_number.survey_language() or "DAN"
    return LANGUAGE_BUTTON_XPATH.format(lang=lang)


def click_element(driver, xpath):
    try:
        element = WebDriverWait(driver, BUTTON_CLICK_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException:
        printer.print_message(f"Timeout when clicking element with xpath: {xpath}")


def select_country_code(driver, phone_number: PhoneNumber):
    click_element(driver, COUNTRY_DROPDOWN_XPATH)
    country_code_xpath = COUNTRY_CODE_XPATH.format(code=phone_number.country_code())
    click_element(driver, country_code_xpath)


def fill_text_field(driver, phone_number):
    try:
        text_field = driver.find_element(By.XPATH, PHONE_FIELD_XPATH)
        WebDriverWait(driver, BUTTON_CLICK_TIMEOUT).until(
            EC.element_to_be_clickable(text_field)
        )
        text_field.clear()
        text_field.send_keys(phone_number.national_number())
    except NoSuchElementException:
        printer.print_message(f"Text field with xpath {PHONE_FIELD_XPATH} not found.")


def send_survey(driver, url, phone_number):
    navigate_to_url(driver, url)
    language_xpath = pick_language_button_xpath(phone_number)
    click_element(driver, language_xpath)
    select_country_code(driver, phone_number)
    fill_text_field(driver, phone_number)
    click_element(driver, SEND_BUTTON_XPATH)


def send_surveys(url, phone_numbers: list):
    driver = initialize_driver()
    sent_to = []

    for phone_number in phone_numbers:
        try:
            send_survey(driver, url, phone_number)
            sent_to.append(phone_number)
            time.sleep(1)  # Wait for page reload
        except Exception as e:
            printer.print_message(f"Error sending to {phone_number.number()}: {e}")
            continue

    printer.print_report(phone_numbers, sent_to)
    driver.quit()
