
def print_greeting():
    greeting_string = "Velkommen til Survey Sender v.2.5.\n\nFor at sende spørgeskemaer:\n1. Vælg excel-filen med telefonnumre fra OneDrive-mappen\n2. Vælg link-type (vælg live link, med mindre du tester sending til dit eget nummer)\n3. Tryk på Send-knappen\n4. Vent på, at programmet har kørt færdig (Hold firefox-vinduet åbent mens det kører)\n5. Åbn excel-filen og slet telefonnumrene der er blevet sendt til. \n\nHvis du har spørgsmål, så kontakt Victor på 52 13 72 34. Hvis du oplever fejl, så send et billede af fejlmeddelelsen og så meget af den øvrige skærm som muligt til Victor på teams eller mail vhm@kattegatcentret.dk"
    print(greeting_string)


def print_imported_numbers(phone_numbers):
    print("----------------------------------")
    print(f"FØLGENDE {len(phone_numbers)} TELEFONNUMRE ER IMPORTERET \n")
    print_list(phone_numbers)


def print_sent_numbers(phone_numbers):
    print("Sendt til antal numre: " + str(len(phone_numbers)) + "\n")
    print_list(phone_numbers)


def print_list(phone_numbers):
    print("INDEX\tTLF.\tLAND\tLANDEKODE")
    # uses enumerate to get index of iteration
    for i, phone_number in enumerate(phone_numbers):
        # converted to string to print
        print(str(i+1), '\t', str(phone_number.national_number()), '\t',
              str(phone_number.region_code()), '\t', str(phone_number.country_code()))


def print_all_sent(sent_to_count):
    print("----------------------------------")
    print(f"SENDING GENNEMFØRT - DER ER SENDT TIL ALLE {sent_to_count} NUMRE")
    print("\nHusk at slette telefonnumrene fra excel-arket, så det er klar til i morgen.")


def print_not_all_sent(phone_numbers, sent_to):
    print("----------------------------------")
    print(
        f"FØLGENDE {len(sent_to)} UD AF {len(phone_numbers)} NUMRE ER SENDT TIL:")
    print_list(sent_to)
    print("Slet disse numre fra excel-arket og prøv igen med resten.")


def print_permission_error_message():
    permission_error_string = "Der er ikke adgang til excel-filen. Sikr dig at filen ikke er åbent i et andet vindue og prøv igen."
    print(permission_error_string)


def print_type_error_message():
    type_error_string = "Ingen data importeret. Vælg en excel-fil med gyldigt indhold og prøv igen."
    print(type_error_string)
