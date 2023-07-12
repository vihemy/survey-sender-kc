#External libraries
import openpyxl

# Internal libraries
from phonenumber_class import PhoneNumber
import printer

def import_numbers_from_excel_as_list(excel_file, first_row, first_col):
    # Sets workbook and sheet for openpyxl
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active # gets active/first sheet-name of workbook
    phone_numbers = [] # resets list
    # loops through specified columns and rows.
    for col in range(first_col, sheet.max_column+1):
        for row in range(first_row, sheet.max_row+1):
            cell = sheet.cell(row, col)
            if cell.value and type(cell.value) == int: # if cell.value is not empty and is an integer
                phone_number = PhoneNumber(cell.value) # creates PhoneNumber-object
                phone_numbers.append(phone_number) # appends phone_number to list
    wb.close() # closes workbook

    printer.print_imported_numbers(phone_numbers)
    return phone_numbers


#----------------------------------

# REMOVED BECAUSE OF SYNC-ISSUES WHEN EDITING FILE ON ONEDRIVE THROUGH SCRIPT

# def clear_sheet(excel_file, first_row, first_col):
#     wb = openpyxl.load_workbook(excel_file)
#     sheet = wb.active
#     for col in range(first_col, sheet.max_column+1):
#         for row in range(first_row, sheet.max_row+1):
#             cell = sheet.cell(row, col)
#             cell.value = None
#     wb.save(excel_file)
#     wb.close()
#     print("Excel-ark er ryddet")
