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
    """Click button based on xpath"""
    try:
        element_present = expected_conditions.presence_of_element_located(
            (By.XPATH, xpath))
        # delays until element is present
        WebDriverWait(driver, delay).until(element_present)
    except TimeoutException:
        print("\nTimed out waiting for page to load")
    else:
        button_to_click = driver.find_element(By.XPATH, xpath)
        # uses javascript to execute click. (Seleniums click function, needed to have button in view, which was problematic.)
        driver.execute_script("arguments[0].click();", button_to_click)


def select_country_code_from_dropdown(driver, phone_number: PhoneNumber):
    """Find and select country_code on dropdown."""
    # (does not use Selenium.Select due to custom dropdown)
    dropdown = driver.find_element(By.CLASS_NAME, "cc-picker")
    # Click dropwdown to expand the options
    dropdown.click()
    # creates xpath expression to search for desired item in the dropdown
    xpath_expression = f'//span[@class="cc-picker-code" and text()="{phone_number.country_code()}"]'

    # find the desired item in the dropdown
    try:
        desired_item = driver.find_element(By.XPATH, xpath_expression)
        desired_item.click()
    except NoSuchElementException:
        print("\nDesired item not found in the dropdown.")
    except Exception as e:
        print(f"\nAn error occurred while selecting the item: {e}")


def insert_number_in_text_field(driver, xpath, phone_number):
    """Find text field and insert national number."""
    text_field = driver.find_element(By.XPATH, xpath)
    text_field.clear()  # clear in case of previous input
    # send_keys is Seleniums equivalent of typing in the text field
    text_field.send_keys(phone_number.national_number())


def scroll_to_bottom(driver):
    """Scroll to the bottom of the screen, to make sure proper element is in view (uses javascript)"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


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
            language_button_xpath = pick_language_button_xpath(
                phone_number)  # uses in survey_language
            click_button(driver, language_button_xpath, delay)

            # Select areacode
            select_country_code_from_dropdown(
                driver, phone_number)  # uses country code

            # Insert phone number
            insert_number_in_text_field(
                driver, '//input[@id="_Q1_O1"]', phone_number)  # uses national_number

            # Presss send
            scroll_to_bottom(driver)
            click_button(driver, '//input[@value="Send"]', delay)
            # Add to sent_to list
            sent_to.append(phone_number)

            # needed for reload of page
            time.sleep(1)

        except TimeoutException:
            print(
                f"\nSiden til sending af nummer: {phone_number.number()} har brugt for lang tid på at laode. Fortsætter til næste nummer")
            continue

        except Exception as e:
            print(
                f"\nUnder afsending af et spørgeskema er følgende fejl er opstået, og har afbrudt sending af spørgeskemaer: {e}")
            break

    print_report(phone_numbers, sent_to)
    driver.quit()
