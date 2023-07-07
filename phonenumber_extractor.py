import openpyxl
import phonenumbers

def import_numbers_from_excel_as_list(excel_file, first_row, first_col):
    # Sets workbook and sheet for openpyxl
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active # gets active/first sheet-name of workbook
    phone_numbers = [] # resets list
    # loops through specified columns and rows.
    for col in range(first_col, sheet.max_column+1):
        for row in range(first_row, sheet.max_row+1):
            cell = sheet.cell(row, col)
            if cell.value: #and type(cell.value) == int:
                phone_numbers.append(str(cell.value)) # appends cell.value to phonenumbers - converts to string to have the plus-sign. (if saved as int, the plus-sign is removed, which makes it impossible for parse_numbers to determine if countrycode)
    wb.close() # closes workbook
    return phone_numbers

def parse_numbers(phone_numbers):
    # Parses phone_numbers into national number and country codesaved as tuples in parsed_numbers. Needs +-sign in front of country code. 
    parsed_phone_numbers = []
    phone_numbers_string = map(str, phone_numbers) # Makes sure that all numbers are converted to string to be used by phonenumbers.parse. (is converted in import_numbers_from_excel_as_list also)

    # loops through phonenumbers and parses them
    for i in phone_numbers_string:
        if '+' in i: # If country code (signified by use of +(!)).
            parsed_number = phonenumbers.parse(i, None) # No need for second argument, as country code is present in i.)
            parsed_phone_numbers.append((parsed_number.national_number, parsed_number.country_code)) # appends national number and country code as tuple to parsed_phone_numbers
        else: # If no country code is present signified by lack of "+"
            parsed_phone_numbers.append(((i), 45)) # if no country code is present, only national number is appended to parsed_phone_numbers.
    return parsed_phone_numbers

 #---------------------------------------------------------------------------------------------------------------------

# CALLS ALL FUNCTIONS ABOVE
def import_and_parse_numbers(excel_file, first_row, first_col):
    phone_numbers = import_numbers_from_excel_as_list(excel_file, first_row, first_col)
    parsed_phone_numbers = parse_numbers(phone_numbers) # Parses numbers in to list of tuples containing national number and country code.
    print("SAMLET ANTAL TELEFONNUMRE: " + str(len(parsed_phone_numbers)) + "\nTELEFONNUMRE (telefonnummer, landekode): \n"+ str(parsed_phone_numbers))
    return parsed_phone_numbers