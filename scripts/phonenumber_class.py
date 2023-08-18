# External modules
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE


class PhoneNumber:
    '''
    Class to handle phone numbers and their characeristics

    Attributes
    ----------
    number : str
        Phone number (e.g. +4512345678)

    Methods
    -------
    number_as_int()
        Returns phone number as int (e.g. 4512345678)
    national_number()
        Returns national number as int (e.g. 12345678)
    country_code()
        Returns country code as int (e.g. 45)
    survey_language()
        Returns survey language as str (e.g. 'DAN')
    region_code()
        Returns region code(s) as tuple of str (e.g. 'DK')
    country_name()
        Returns country name as str (e.g. 'Denmark')
    '''

    def __init__(self, number):
        self.number = number

    def number_as_int(self):
        """Return phone number as int (e.g. 4512345678)"""
        number_as_int = int(self.number)
        return number_as_int

    def national_number(self):
        """Return national number as int (e.g. 12345678)"""
        # If country code is noted (signified by use of +), country code is stripped, leaving only national number - OBS! THIS IS STRING, NOT INT! PLUS-SIGN CAN NOT BE DETECTED IN INT!
        if self._starts_with_plus(self.number):
            # No need for second argument, as country code is present in i.)
            parsed_number = phonenumbers.parse(self.number, None)
            national_number = parsed_number.national_number

        # If no country code is present (signified by lack of "+") all of self.number is national number
        else:
            national_number = int(self.number)
        return national_number

    def country_code(self):
        """Return country code as int (e.g. 45). If no country code is present, country code is set to 45 (Denmark)"""
        # if '+' in self.number:
        if self._starts_with_plus(self.number):
            parsed_number = phonenumbers.parse(self.number, None)
            country_code = parsed_number.country_code
        else:
            country_code = 45
        return country_code

    def _starts_with_plus(self, number):
        """Return True if number starts with '+', False if not"""
        if number[0] == '+':
            return True
        else:
            return False

    def survey_language(self):
        """Return survey language as str (e.g. 'DAN')"""
        if self.country_code() == 45:
            survey_language = 'DAN'
        elif self.country_code() == 49 or self.country_code() == 43 or self.country_code() == 41:
            survey_language = 'DEU'
        else:
            survey_language = 'ENG'
        return survey_language

    def region_code(self):
        """Return region code(s) as tuple of str (e.g. 'DK')"""
        region_code = COUNTRY_CODE_TO_REGION_CODE[self.country_code()]
        return region_code

    def country_name(self):
        """Return country name as str (e.g. 'Denmark')"""
        if '+' in self.number:
            # Gets country name from number
            parsed_number = phonenumbers.parse(self.number, None)
            country_name = geocoder.country_name_for_number(
                parsed_number, "en")
        # If no country code is present (signified by lack of "+")
        else:
            country_name = "Denmark"
        return country_name
