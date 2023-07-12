
def print_greeting():
    greeting_string = "Velkommen til Survey Sender v.2.0.\n\nFor at sende spørgeskemaer, gør følgende:\n1. Vælg excel-filen med telefonnumre fra OneDrive-mappen\n2. Vælg link-type (vælg live link, med mindre du tester sending til dit eget nummer\n3. Tryk på Send-knappen\n4. Vent på, at programmet har kørt færdig\n5. Åbn excel-filen og slet telefonnumrene der er blevet sendt til. \n\nHvis du har spørgsmål, så kontakt Victor på 52 13 72 34. Hvis du oplever fejl, så send et billede af skærmen til Victor på teams eller mail vhm@kattegatcentret.dk"
    print(greeting_string)

    #_______________________________________________________________________________________________

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

def print_all_sent():
    print("----------------------------------")
    print("ALLE NUMRE BLEV SENDT")
    print("\nHUSK AT SLETTE NUMRENE FRA EXCEL-ARKET")

def print_not_all_sent(phone_numbers, sent_to):
    print("----------------------------------")
    print(f"{len(phone_numbers) - len(sent_to)} NUMRE BLEV IKKE SENDT. FØLGENDE NUMRE ER DOG SENDT:")
    print_list(sent_to)
    print("SLET OVERSTÅENDE NUMRE FRA EXCEL-ARKET OG PRØV IGEN")

#_______________________________________________________________________________________________

def print_permission_error_message():
    permission_error_string = "Der er ikke adgang til excel-filen. Luk excel-filen, hvis du har den åbent et andet sted på computeren og prøv igen."
    print(permission_error_string)

def print_type_error_message():
    type_error_string = "Ingen data importeret. Vælg en excel-fil med gyldigt indhold og prøv igen."
    print(type_error_string)

