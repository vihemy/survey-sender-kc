# External modules
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE


class PhoneNumber:
    """
    Class to handle phone numbers and their characteristics.

    Attributes
    ----------
    number : str
        Phone number (e.g. +4512345678)
    parsed_number : PhoneNumber object
        Parsed phone number object from the phonenumbers library

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
    """

    COUNTRY_LANGUAGE_MAP = {
        45: "DAN",  # Denmark
        49: "DEU",  # Germany
        43: "DEU",  # Austria
        41: "DEU",  # Switzerland
        # Add other mappings as needed
    }

    def __init__(self, number):
        if number.startswith("00"):
            self.number = "+" + number[2:]
        else:
            self.number = number
        self.parsed_number = (
            phonenumbers.parse(self.number, None)
            if self.number.startswith("+")
            else None
        )

    def number_as_int(self):
        """Return phone number as int (e.g. 4512345678)"""
        return int(self.number)

    def national_number(self):
        """Return national number as int (e.g. 12345678)"""
        return (
            self.parsed_number.national_number
            if self.parsed_number
            else int(self.number)
        )

    def country_code(self):
        """Return country code as int (e.g. 45). If no country code is present, country code is set to 45 (Denmark)"""
        return self.parsed_number.country_code if self.parsed_number else 45

    def survey_language(self):
        """Return survey language as str (e.g. 'DAN')"""
        return self.COUNTRY_LANGUAGE_MAP.get(self.country_code(), "ENG")

    def region_code(self):
        """Return region code(s) as tuple of str (e.g. 'DK')"""
        return COUNTRY_CODE_TO_REGION_CODE.get(self.country_code(), ("Unknown",))

    def country_name(self):
        """Return country name as str (e.g. 'Denmark')"""
        return (
            geocoder.country_name_for_number(self.parsed_number, "en")
            if self.parsed_number
            else "Denmark"
        )
