#External libraries
import openpyxl

# Internal libraries
from phonenumber_class import PhoneNumber

def import_numbers_from_excel_as_list(excel_file, first_row, first_col):
    # Sets workbook and sheet for openpyxl
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active # gets active/first sheet-name of workbook
    phone_numbers = [] # resets list
    # loops through specified columns and rows.
    for col in range(first_col, sheet.max_column+1):
        for row in range(first_row, sheet.max_row+1):
            cell = sheet.cell(row, col)
            if cell.value: # if cell.value is not empty
                phone_number = PhoneNumber(cell.value) # creates PhoneNumber-object
                phone_numbers.append(phone_number) # appends phone_number to list
    wb.close() # closes workbook

    print_imported_numbers(phone_numbers)
    return phone_numbers

def print_imported_numbers(phone_numbers):
    print("----------------------------------")
    print("SAMLET ANTAL TELEFONNUMRE: " + str(len(phone_numbers)) + "\n")
    print ("NUMMER / LANDEKODE")

    for phone_number in phone_numbers:
        print(str(phone_number.national_number()) + " / " + str(phone_number.country_code())) # converted to string to print
    return phone_numbers

def print_sent_numbers(phone_numbers):
    print("----------------------------------")
    print("SPØRGESKEMA SENDT TIL ANTAL TELEFONNUMRE: " + str(len(phone_numbers)) + "\n")
    print ("NUMMER / LANDEKODE")

    for phone_number in phone_numbers:
        print(phone_number.national_number(), phone_number.country_code())
    return phone_numbers

def clear_sheet(excel_file, first_row, first_col):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    for col in range(first_col, sheet.max_column+1):
        for row in range(first_row, sheet.max_row+1):
            cell = sheet.cell(row, col)
            cell.value = None
    wb.save(excel_file)
    wb.close()
    print("Excel-ark er ryddet")
