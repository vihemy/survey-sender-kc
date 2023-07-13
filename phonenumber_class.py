import phonenumbers  # Library for parsing phone numbers


class PhoneNumber:
    def __init__(self, number):
        self.number = number

    def number_as_int(self):
        number_as_int = int(self.number)
        return number_as_int

    def national_number(self):
        # If country code is noted (signified by use of +), country code is stripped, leaving only national number - OBS! THIS IS STRING, NOT INT! PLUS-SIGN CAN NOT BE DETECTED IN INT!
        if '+' in self.number:
            # No need for second argument, as country code is present in i.)
            parsed_number = phonenumbers.parse(self.number, None)
            national_number = parsed_number.national_number

        # If no country code is present (signified by lack of "+") all of self.number is national number
        else:
            national_number = int(self.number)
        return national_number

    # Gets country code from number. If no country code is present, country code is set to 45 (Denmark)
    def country_code(self):
        if '+' in self.number:
            parsed_number = phonenumbers.parse(self.number, None)
            country_code = parsed_number.country_code
        else:
            country_code = 45
        return country_code

    def survey_language(self):  # Gets survey language from country code
        if self.country_code() == 45:
            survey_language = 'DAN'
        elif self.country_code() == 49 or self.country_code() == 43 or self.country_code() == 41:
            survey_language = 'DEU'
        else:
            survey_language = 'ENG'
        return survey_language
