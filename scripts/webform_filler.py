# External libraries
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

# Internal libraries
from phonenumber_class import PhoneNumber
import printer


def initialize_driver():
    """Initialize the Firefox driver and return it"""
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
    """Open the webform in Firefox"""
    driver.get(url)


def pick_language_button_xpath(phone_number: PhoneNumber):
    """Return xpath for language button based on Phonenumber instances survey_language."""
    # Selenium uses xpath to find elements in html.
    if not phone_number.survey_language():  # if survey_language is None default to danish
        xpath = '//input[@value="DAN"]'
    else:  # choose form-language based on survey_language
        xpath = f'//input[@value="{phone_number.survey_language()}"]'
    return xpath


def click_button(driver, xpath, delay):
    """Click a button based on given xpath using executive_script (javascript)"""
    try:
        WebDriverWait(driver, delay).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print("Page load timed out")
    else:
        button_to_click = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_to_click)


def select_country_code_from_dropdown(driver, phone_number: PhoneNumber):
    """Open dropdown, find dropdown-item with country_code, select item from."""
    dropdown_xpath = "//div[@class='cc-picker cc-picker-code-select-enabled']"
    click_button(driver, dropdown_xpath, 5)
    item_xpath = f'//span[@class="cc-picker-code" and text()="{phone_number.country_code()}"]'
    click_button(driver, item_xpath, 5)


def fill_text_field(driver, xpath, phone_number):
    """Find text field and insert national number."""
    text_field = driver.find_element(By.XPATH, xpath)
    # Waits x secs if element is not yet visible
    WebDriverWait(driver, 3000).until(
        expected_conditions.element_to_be_clickable((text_field)))
    # clear in case of previous input
    text_field.clear()
    # send_keys is Seleniums equivalent of typing in the text field
    text_field.send_keys(phone_number.national_number())


def scroll_to_bottom(driver):
    """Scroll to the bottom of the screen, to make sure proper element is in view (uses javascript)"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_to_element(driver, element):
    """Scroll to element, to make sure it'n in view (uses javascript and scrollIntoView in stead of Seleniums moveToElement, that changes curser position)"""
    driver.execute_script("arguments[0].scrollIntoView();", element)


def print_report(phone_numbers, sent_to):
    """Print report of sendings to user."""
    if len(phone_numbers) > len(sent_to):  # if not all numbers were sent
        printer.print_not_all_sent(phone_numbers, sent_to)
    if len(phone_numbers) == len(sent_to):  # if all numbers were sent
        printer.print_all_sent(len(sent_to))
    else:  # default message
        printer.print_all_sent(len(sent_to))


# CALLS ALL FUNCTIONS ABOVE
def send_surveys(url, phone_numbers: list):
    """Send surveys to phone numbers in list"""
    driver = initialize_driver()
    open_webform(driver, url)
    delay = 5  # delay for click_buttonScripts
    sent_to = []

    for phone_number in phone_numbers:
        try:
            # Choose one of three languages
            language_button_xpath = pick_language_button_xpath(phone_number)
            click_button(driver, language_button_xpath, delay)

            # Select areacode
            select_country_code_from_dropdown(driver, phone_number)

            # Insert phone number
            fill_text_field(driver, '//input[@id="_Q1_O1"]', phone_number)

            # Presss send
            click_button(driver, '//input[@value="Send"]', delay)

            # Add to sent_to list
            sent_to.append(phone_number)

            # needed for reload of page
            time.sleep(1)

        except Exception as e:
            print(
                f"\nVed sending til nummer: {phone_number.number()} er følgende fejl er opstået: \n {e} \n Fortsætter til næste nummer")
            continue

    print_report(phone_numbers, sent_to)
    driver.quit()
