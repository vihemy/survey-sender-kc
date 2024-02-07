# External libraries
import sys
import os
import PySimpleGUI as sg

# Internal libraries
import excel_processor
import webform_handler
import printer

# Inspiration = https://realpython.com/pysimplegui-python/


def default_excel_path():
    """Return default path to excel file as str."""
    if getattr(sys, "frozen", False):
        application_directory = os.path.dirname(sys.executable)
    else:
        application_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    return os.path.join(
        application_directory, "Liste til telefonnumre - Tilfredshedsundersøgelse.xlsx"
    )


def create_layout(excel_file):
    """Create and return the layout for the PySimpleGUI window."""
    return [
        [
            sg.Text("Excel fil sti: "),
            sg.Input(excel_file, key="-FILEPATH-"),
            sg.FileBrowse(),
        ],
        [sg.Button("Importer", key="-IMPORT-")],
        [sg.Output(size=(80, 20), key="-OUTPUT-")],
        [sg.Text("Vælg link:"), sg.Combo(["Test link", "Live link"], key="-COMBO-")],
        [sg.Button("Send", key="-SEND-"), sg.Button("Exit", key="-EXIT-")],
    ]


def handle_import_event(values):
    """Handle import event to read phone numbers from Excel."""
    try:
        excel_file = values["-FILEPATH-"]
        phone_numbers = excel_processor.import_numbers_from_excel_as_list(
            excel_file, first_row, first_column
        )
        return phone_numbers
    except PermissionError:
        printer.print_permission_error_message()
    except Exception as e:
        log_exception(e)


def handle_send_event(values, phone_numbers):
    """Handle the event when the 'Send' button is pressed."""
    try:
        url = get_survey_url(values["-COMBO-"])
        webform_handler.send_surveys(url, phone_numbers)
    except PermissionError:
        printer.print_permission_error_message()
    except TypeError:
        printer.print_type_error_message()
    except Exception as e:
        log_exception(e)


def get_survey_url(combo_value):
    """Returns the appropriate survey URL based on the combo box selection."""
    if combo_value == "":
        raise TypeError("Intet link valgt")
    elif combo_value == "Test link":
        return "https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1&test=1"
    elif combo_value == "Live link":
        return "https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1"
    else:
        raise ValueError("Invalid link choice")


def log_exception(exception):
    """Logs the exception details."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error_message = (
        f"DER ER OPSTÅET EN FEJL: {exception}{exc_type}{fname}{exc_tb.tb_lineno}"
    )
    print(error_message)
    # Consider adding logging to a file here


# Initialize variables
excel_file = default_excel_path()
first_row = 8
first_column = 1
phone_numbers = []

# Choose Theme
sg.theme("BlueMono")

# Create the PySimpleGUI layout
layout = create_layout(excel_file)

# Create the window with PySimpleGUI
window = sg.Window("Survey Sender v.2.5", layout, finalize=True)
printer.print_greeting()

# Event loop to process events and update window
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "-EXIT-":
        break
    elif event == "-IMPORT-":
        phone_numbers = handle_import_event(values)
    elif event == "-SEND-":
        handle_send_event(values, phone_numbers)

window.close()
