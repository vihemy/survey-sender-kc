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
    print("ANTAL IMPORTEDE TELEFONNUMRE : " + str(len(phone_numbers)) + "\n")
    print_list(phone_numbers)

def print_sent_numbers(phone_numbers):
    print("----------------------------------")
    print("SENDT TIL ANTAL TELEFONNUMRE: " + str(len(phone_numbers)) + "\n")
    print_list(phone_numbers)

def print_list(phone_numbers):
    print ("INDEX - TLF.NUMMER")
    for i, phone_number in enumerate(phone_numbers): # uses enumerate to get index of iteration
        print(str(i+1) + " - " + str(phone_number.number_as_int())) # converted to string to print

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
