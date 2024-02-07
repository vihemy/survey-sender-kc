import openpyxl
import re
from phonenumbers import NumberParseException
from phonenumber_class import PhoneNumber
import printer

INVALID_CHARS_PATTERN = re.compile(r"[^0-9+]")


def is_cell_valid(cell):
    """Check if cell content is valid."""
    if (
        cell.value is None
        or len(cell.value) < 8
        or INVALID_CHARS_PATTERN.search(cell.value)
    ):
        return False
    return True


def import_phone_numbers(excel_file, first_row, first_col):
    """Import phone numbers from excel file and return as list of PhoneNumber-objects"""
    phone_numbers = []  # resets list
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active  # gets active/first sheet-name of workbook
    try:
        for col in range(first_col, sheet.max_column + 1):
            for row in range(first_row, sheet.max_row + 1):
                cell = sheet.cell(row, col)
                if not is_cell_valid(cell):
                    continue
                try:
                    phone_number = PhoneNumber(cell.value)
                    phone_numbers.append(phone_number)
                except NumberParseException:
                    print(
                        f"Række {row}, kolonne {col} indeholder ugyldigt telefonnummer. Nummeret er ikke blevet importeret."
                    )
                continue
    except Exception as e:
        print(f"Kunne ikke åbne eller læse excel-filen: {e}")

    wb.close()  # closes workbook
    printer.print_imported_numbers(phone_numbers)
    return phone_numbers
