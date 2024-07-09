from FIRMY import show_companies, add_company, remove_company, update_company, companies_map, language_search
from KLIENCI import show_clients, add_client, remove_client, update_client, clients_map
from PRACOWNICY import show_workers, add_worker, remove_worker, update_worker, workers_map

from Dane_osobowe import companies, clients, workers

def logowanie():
    correct_login = "projektowanie"
    correct_password = "1234"
    logowanie = False

    while not logowanie:
        login = input("Wprowadź login: ")
        password = input("Wprowadź hasło: ")

        if login == correct_login and password == correct_password:
            print("Pomyślnie zalogowano.")
            logowanie = True
        else:
            print("Niepoprawny login lub hasło.")
    return logowanie


if logowanie():
    if __name__ == '__main__':
        print("Witaj w systemie zarządzania firmami tłumaczeniowymi.")
        while True:
            print("Menu:")
            print("0. Zakończ pracę")
            print("1. Firmy Tłumaczeniowe")
            print("2. Klienci")
            print("3. Pracownicy")
            menu_option = input("Wybierz opcję: ")
            if menu_option == '0':
                break
            elif menu_option == '1':
                while True:
                    print("0. Powrót do menu głównego")
                    print("1. Wyświetl listę firm tłumaczeniowych")
                    print("2. Dodaj firmę do listy")
                    print("3. Usuń firmę z listy")
                    print("4. Aktualizuj dane firmy")
                    print("5. Wyświetl lokalizację wszystkich firm na mapie")
                    print("6. Szukaj języka")
                    opcja = input("Wybierz opcję: ")
                    if opcja == '0':
                        break
                    elif opcja == '1':
                        show_companies(companies)
                    elif opcja == '2':
                        add_company(companies)
                        show_companies(companies)
                    elif opcja == '3':
                        remove_company(companies)
                        show_companies(companies)
                    elif opcja == '4':
                        update_company(companies)
                        show_companies(companies)
                    elif opcja == '5':
                        companies_map(companies)
                    elif opcja == '6':
                        language_search(companies)
                    else:
                        print("Niewłaściwa opcja. Wybierz z dostępnych powyżej")
            elif menu_option == '2':
                while True:
                    print("0. Powrót do menu głównego")
                    print("1. Wyświetl listę klientów danej firmy")
                    print("2. Dodaj klienta do firmy")
                    print("3. Usuń klienta z firmy")
                    print("4. Aktualizuj dane klienta")
                    print("5. Wyświetl lokalizację wszystkich klientów na mapie")

                    opcja = input("Wybierz opcję: ")
                    if opcja == '0':
                        break
                    elif opcja == '1':
                        show_clients(clients)
                    elif opcja == '2':
                        add_client(clients, companies)
                    elif opcja == '3':
                        remove_client(clients, companies)
                    elif opcja == '4':
                        update_client(clients, companies)
                    elif opcja == '5':
                        clients_map(clients)

                    else:
                        print("Niewłaściwa opcja. Wybierz z dostępnych powyżej.")
            elif menu_option == '3':
                while True:
                    print("0. Powrót do menu głównego")
                    print("1. Wyświetl listę pracowników danej firmy")
                    print("2. Dodaj pracownika do firmy")
                    print("3. Usuń pracownika z firmy")
                    print("4. Aktualizuj dane pracownika")
                    print("5. Wyświetl lokalizację wszystkich pracowników na mapie")
                    opcja = input("Wybierz opcję: ")
                    if opcja == '0':
                        break
                    elif opcja == '1':
                        show_workers(workers)
                    elif opcja == '2':
                        add_worker(workers, companies)
                    elif opcja == '3':
                        remove_worker(workers, companies)
                    elif opcja == '4':
                        update_worker(workers, companies, )
                    elif opcja == '5':
                        workers_map(workers)
                    else:
                        print("Niewłaściwa opcja. Wybierz z dostępnych powyżej.")
            print("Dziękujemy za skorzystanie z systemu. Do widzenia!")
