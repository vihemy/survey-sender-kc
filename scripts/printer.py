DIVIDER = "----------------------------------"
GREETING_MESSAGE = (
    "Velkommen til Survey Sender v.2.5.\n\n"
    "For at sende spørgeskemaer:\n"
    "1. Vælg excel-filen med telefonnumre fra OneDrive-mappen\n"
    "2. Vælg link-type (vælg live link, med mindre du tester sending til dit eget nummer)\n"
    "3. Tryk på Send-knappen\n"
    "4. Vent på, at programmet har kørt færdig (Hold firefox-vinduet åbent mens det kører)\n"
    "5. Åbn excel-filen og slet telefonnumrene der er blevet sendt til. \n\n"
    "Hvis du har spørgsmål, så kontakt Victor på 52 13 72 34. "
    "Hvis du oplever fejl, så send et billede af fejlmeddelelsen og resten af computerskærmen til Victor på teams eller mail vhm@kattegatcentret.dk"
)


def print_message(header, body=""):
    print(DIVIDER)
    if header:
        print(header)
    if body:
        print(body)
    print(DIVIDER)


def print_greeting():
    print_message(GREETING_MESSAGE)


def print_phone_numbers(title, phone_numbers):
    header = f"{title} {len(phone_numbers)} TELEFONNUMRE"
    body = "INDEX\tTLF.\tLAND\tLANDEKODE\n" + "\n".join(
        f"{i+1}\t{phone_number.national_number()}\t"
        f"{phone_number.region_code()}\t{phone_number.country_code()}"
        for i, phone_number in enumerate(phone_numbers)
    )
    print_message(header, body)


def print_imported_numbers(phone_numbers):
    print_phone_numbers("IMPORT FULDFØRT:", phone_numbers)


def print_sent_numbers(phone_numbers):
    print_phone_numbers("Sendt til antal numre", phone_numbers)


def print_all_sent(sent_to_count):
    print_message(
        f"SENDING GENNEMFØRT - DER ER SENDT TIL ALLE {sent_to_count} NUMRE",
        "Husk at slette telefonnumrene fra excel-arket, så det er klar til i morgen.",
    )


def print_not_all_sent(phone_numbers, sent_to):
    print_phone_numbers(
        f"FØLGENDE {len(sent_to)} UD AF {len(phone_numbers)} NUMRE ER SENDT TIL",
        sent_to,
    )
    print("Slet disse numre fra excel-arket og prøv igen med resten.")


def print_permission_error_message():
    print_message(
        "Adgangsfejl",
        "Der er ikke adgang til excel-filen. Sikr dig at filen ikke er åbent i et andet vindue og prøv igen.",
    )


def print_type_error_message():
    print_message(
        "Importfejl",
        "Ingen data importeret. Vælg en excel-fil med gyldigt indhold og prøv igen.",
    )


def print_report(phone_numbers, sent_to):
    """Print report of sendings to user."""
    if len(phone_numbers) > len(sent_to):  # if not all numbers were sent
        print_not_all_sent(phone_numbers, sent_to)
    if len(phone_numbers) == len(sent_to):  # if all numbers were sent
        print_all_sent(len(sent_to))
    else:  # default message
        print_all_sent(len(sent_to))
