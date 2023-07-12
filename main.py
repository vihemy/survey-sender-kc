# External libraries
import sys
import os
import PySimpleGUI as sg

# Internal libraries
import phonenumber_extractor
import webform_filler

#Inspiration = https://realpython.com/pysimplegui-python/ 

# Define the Excel file path and sheet name
# folder_directory = Path( __file__ ).parent.absolute() # gets current folder of script
# file_directory = folder_directory.joinpath("Liste til telefonnumre - Tilfredshedsundersøgelse.xlsx") # gets file and joins it with folder path
# excel_file = file_directory

excel_file = ''
first_row = 8
first_column = 1
#url = 'https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1&test=1' # TEST URL

permission_error_string = "Der er ikke adgang til excel-filen. Luk excel-filen, hvis du har den åbent et andet sted på computeren og prøv igen."
type_error_string = "Ingen data importeret. Vælg en excel-fil med gyldigt indhold og prøv igen."

#_________________________________________________________PYSIMPLEGUI_______________________________________________________

#Choose Theme
sg.theme('BlueMono') # theme-overview: https://www.geeksforgeeks.org/themes-in-pysimplegui/

    # Create the PySimpleGUI layout
layout = [
    [sg.Text('Excel fil sti: '), sg.Input(excel_file, key= '-FILEPATH-'), sg.FileBrowse()],
    [sg.Button('Importer', key="-IMPORT-")],
    [sg.Output(size=(80,20), key="-OUTPUT-")],
    [sg.Text("Vælg link:"), sg.Combo(["Test link", "Live link"], key="-COMBO-")],
    [sg.Button('Send', key="-SEND-"), sg.Button('Slet telefonnumre fra fil', key="-DELETE-"), sg.Button('Exit', key="-EXIT-")]
]

# Create the window with PySimpleGUI
window = sg.Window('Survey Sender v.2', layout)

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
            phone_numbers = phonenumber_extractor.import_numbers_from_excel_as_list(excel_file, first_row, first_column)
        except PermissionError:
            print(permission_error_string)  
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"An error occurred: {e}{exc_type}{fname}{exc_tb.tb_lineno}")
            
    # Calls send_surveys-function with updated variables
    elif event == "-DELETE-":
        try:
            excel_file = values['-FILEPATH-'] 
            # Display a confirmation prompt before executing the script
            confirm = sg.popup_yes_no("Er du sikker på, at du vil slette telefonnumrene fra excel-arket?", title="Bekræftelse")
            if confirm == "Yes":
                phonenumber_extractor.clear_sheet(excel_file, first_row, first_column)
                sg.popup("Cellerne er blevet slettet.", title="Færdig")
        except PermissionError:
            print(permission_error_string)          
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() # defines exception-information
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
            print(permission_error_string)    
        except TypeError:
            print(type_error_string)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"DER ER OPSTÅET EN FEJL. SEND ET BILLEDE AF SKÆRMEN OG FØLGENDE FEJLMEDDELELSE TIL VICTOR:\n{e}{exc_type}{fname}{exc_tb.tb_lineno}")