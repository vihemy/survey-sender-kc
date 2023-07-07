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
first_col = 1
#url = 'https://study.epinionglobal.com/ta_e/kattegatcentret?abs=1&seg=1&test=1' # TEST URL


#_________________________________________________________PYSIMPLEGUI_______________________________________________________


    # Create the PySimpleGUI layout
layout = [
    [sg.Text('Excel fil sti: '), sg.Input(excel_file, key= '-FILEPATH-'), sg.FileBrowse()],
    [sg.Text('Første række med telefonnumre: '), sg.InputText(first_row, key="-FIRSTROW-")],
    [sg.Text('Første kolonne med telefonnumre: '), sg.InputText(first_col, key="-FIRSTCOLUMN-")],
    [sg.Button('Importer', key="-IMPORT-")],
    [sg.Output(size=(80,20), key="-OUTPUT-")],
    [sg.Text("Vælg link:"), sg.Combo(["Test link", "Live link"], key="-COMBO-")],
    [sg.Button('Send', key="-SEND-"), sg.Button('Slet telefonnumre fra fil', key="-DELETE-"), sg.Button('Exit', key="-EXIT-")]
]

# Create the window with PySimpleGUI
window = sg.Window('Survey Sender', layout)

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
            first_row = int(values['-FIRSTROW-'])
            first_column = int(values['-FIRSTCOLUMN-'])
            parsed_phone_numbers = phonenumber_extractor.import_and_parse_numbers(excel_file, first_row, first_column)
        except PermissionError:
            print("Der er ikke adgang til excel-filen. Luk excel-filen og prøv igen.")  
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"An error occurred: {e}{exc_type}{fname}{exc_tb.tb_lineno}")
            
    # Calls send_surveys-function with updated variables
    elif event == "-DELETE-":
        try:
            excel_file = values['-FILEPATH-'] 
            first_row = int(values['-FIRSTROW-'])
            first_column = int(values['-FIRSTCOLUMN-'])
            # Display a confirmation prompt before executing the script
            confirm = sg.popup_yes_no("Er du sikker på, at du vil slette telefonnumrene fra excel-arket?", title="Bekræftelse")
            if confirm == "Yes":
                phonenumber_extractor.clear_sheet(excel_file, first_row, first_column)
                sg.popup("Cellerne er blevet slettet.", title="Færdig")
        except PermissionError:
            print("Der er ikke adgang til excel-filen. Luk excel-filen og prøv igen.")          
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
            webform_filler.send_surveys(url, parsed_phone_numbers)
        except PermissionError:
            print("Der er ikke adgang til excel-filen. Luk excel-filen og prøv igen.")    
        except TypeError:
            print("Ingen data importeret. Vælg en gyldig filsti og prøv igen.")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() # defines exception-information
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"DER ER OPSTÅET EN FEJL. SEND ET BILLEDE AF SKÆRMEN OG FØLGENDE FEJLMEDDELELSE TIL VICTOR:\n{e}{exc_type}{fname}{exc_tb.tb_lineno}")