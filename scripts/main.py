# External libraries
import sys
import os
import PySimpleGUI as sg

# Internal libraries
import phonenumber_extractor
import webform_filler
import printer

# Inspiration = https://realpython.com/pysimplegui-python/


def default_excel_path():
    """Return default path to excel file as str"""
    if getattr(sys, 'frozen', False):
        # If the application is run as a -onefile (pyinstaller) the path is different than if run as a script
        application_directory = os.path.dirname(sys.executable)
    # If not the application is run as onefile (pyinstaller) the path is set to the parent directory of this script
    else:
        application_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))

    excel_file = os.path.join(
        application_directory, "Liste til telefonnumre - Tilfredshedsundersøgelse.xlsx")
    return excel_file


# Initialize variables
excel_file = default_excel_path()
first_row = 8
first_column = 1

# Choose Theme - https://www.geeksforgeeks.org/themes-in-pysimplegui/
sg.theme('BlueMono')

# Create the PySimpleGUI layout
layout = [
    [sg.Text('Excel fil sti: '), sg.Input(
        excel_file, key='-FILEPATH-'), sg.FileBrowse()],
    [sg.Button('Importer', key="-IMPORT-")],
    [sg.Output(size=(80, 20), key="-OUTPUT-")],
    [sg.Text("Vælg link:"), sg.Combo(
        ["Test link", "Live link"], key="-COMBO-")],
    [sg.Button('Send', key="-SEND-"), sg.Button('Exit', key="-EXIT-")]
]

# Create the window with PySimpleGUI
# finalize=True makes it possible to call follow function when window is opened
window = sg.Window('Survey Sender v.2.5', layout, finalize=True)
printer.print_greeting()

# Event loop to process events and update window
while True:
    event, values = window.read()
    # Ends program
    if event == sg.WIN_CLOSED or event == "-EXIT-":
        break
    # Calls import_and_parse_numbers when button Import is pressed
    elif event == "-IMPORT-":
        try:
            excel_file = values['-FILEPATH-']
            phone_numbers = phonenumber_extractor.import_numbers_from_excel_as_list(
                excel_file, first_row, first_column)
        except PermissionError:
            printer.print_permission_error_message()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()  # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"An error occurred: {e}{exc_type}{fname}{exc_tb.tb_lineno}")

    # Calls send_surveys-function with updated variables
    elif event == "-SEND-":
        try:
            # checks for selection of combo. Sets url to appropriate choice.
            if values["-COMBO-"] == '':
                raise TypeError("Intet link valgt")
            elif values["-COMBO-"] == "Test link":
                url = "https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1&test=1"
            elif values["-COMBO-"] == "Live link":
                url = "https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1"
            webform_filler.send_surveys(url, phone_numbers)
        except PermissionError:
            printer.print_permission_error_message()
        except TypeError:
            printer.print_type_error_message()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()  # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(
                f"DER ER OPSTÅET EN FEJL. SEND ET BILLEDE AF SKÆRMEN OG FØLGENDE FEJLMEDDELELSE TIL VICTOR:\n{e}{exc_type}{fname}{exc_tb.tb_lineno}")
