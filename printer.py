

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

def print_not_all_sent(phone_numbers, sent_to):
    print("----------------------------------")
    print(f"{len(phone_numbers) - len(sent_to)} NUMRE BLEV IKKE SENDT. FØLGENDE NUMRE ER DOG SENDT:")

def print_all_sent():
    print("----------------------------------")
    print("ALLE NUMRE BLEV SENDT")