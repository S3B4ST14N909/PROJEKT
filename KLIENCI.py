from bs4 import BeautifulSoup
import requests
import folium
import webbrowser
import os


def get_coords(client_location):
    adres_url = f'https://pl.wikipedia.org/wiki/{client_location}'
    response = requests.get(adres_url)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    print([latitude, longitude])
    return [latitude, longitude]


def show_clients(clients):
    # Wyświetla listę klientów firmy
    company_name = input("Podaj nazwę kliniki, której lista klientów ma zostać wyświetlona: ")
    company_found = False

    # Sprawdzenie, czy firma istnieje wśród klientów
    for client in clients:
        if client['client_company'] == company_name:
            company_found = True
            break

    # Wyświetlenie listy klientów, jeśli firma została znaleziona
    if company_found:
        print(f"Lista klientów kliniki {company_name}:")
        for client in clients:
            if client['client_company'] == company_name:
                print(f" - {client['client_name']}")
    else:
        print(f"{company_name} nie znaleziono takiej kliniki na liście.")


def add_client(clients, companies):
    # Dodaje nowego klienta do firmy
    company_name = input("Podaj nazwę kliniki, do której chcesz dodać klienta: ")
    company_found = False
    for company in companies:
        if company["company_name"] == company_name:
            client_name = input(f"Podaj imię i nazwisko klienta do dodania do {company_name}: ")
            client_location = input(f"Podaj lokalizację klienta (miasto): ")
            company_name = input(f"Podaj Klinikę, której {client_name} jest klientem (klientką): ")
            clients.append({
                "client_name": client_name,
                "client_company": company_name,
                "client_location": client_location
            })
            print(f"{client_name} został(a) dodany(a) do listy klientów kliniki {company_name}.")
            company_found = True
            break
    if not company_found:
        print(f"{company_name} nie znaleziono takiej kliniki na liście.")


def remove_client(clients,companies):
    client_name = input("Podaj imię i nazwisko klienta do usunięcia: ")
    company_name = input("Podaj nazwę kliniki, z której chcesz usunąć klienta: ")

    client_found = False

    for client in clients:
        if client['client_name'] == client_name and client['client_company'] == company_name:
            clients.remove(client)
            client_found = True
            print(f"Klient {client_name} został usunięty z kliniki {company_name}.")
            break

    if not client_found:
        print(f"Nie znaleziono klienta {client_name} w klinice {company_name}.")


def update_client(clients,companies):
    # Pobierz nazwę firmy i imię i nazwisko klienta do aktualizacji
    company_name = input("Podaj nazwę kliniki, w której chcesz zaktualizować dane klienta: ")
    client_name = input("Podaj imię i nazwisko klienta do zaktualizowania: ")

    company_found = False
    client_found = False

    # Sprawdzenie, czy firma istnieje
    for company in companies:
        if company['company_name'] == company_name:
            company_found = True
            break

    if not company_found:
        print(f"Nie znaleziono kliniki o nazwie {company_name}.")
        return

    # Aktualizacja danych klienta
    for client in clients:
        if client['client_name'] == client_name and client['client_company'] == company_name:
            client_found = True
            new_client_name = input("Podaj nowe imię i nazwisko klienta: ")
            new_client_location = input("Podaj nową lokalizację klienta: ")

            client['client_name'] = new_client_name
            client['client_location'] = new_client_location

            print(
                f"Zaktualizowano dane klienta {client_name} na {new_client_name}, lokalizacja: {new_client_location}.")
            break

    if not client_found:
        print(f"Nie znaleziono klienta o imieniu i nazwisku {client_name} w klinice {company_name}.")


def dms_to_decimal(dms):
    parts = dms.split('°')
    degrees = float(parts[0])
    parts = parts[1].split('′')
    minutes = float(parts[0])
    parts = parts[1].split('″')
    seconds = float(parts[0])
    direction = parts[1].strip()

    decimal_degrees = degrees + minutes / 60 + seconds / 3600

    if direction in ['S', 'W']:
        decimal_degrees *= -1

    return decimal_degrees


def clients_map(clients):
    map = folium.Map(location=[52, 20], zoom_start=7)
    for client in clients:
        client_name = client['client_name']
        client_location = client['client_location']
        url = f"https://pl.wikipedia.org/wiki/{client_location}"

        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')

        latitude_tag = response_html.find('span', {'class': 'latitude'})
        longitude_tag = response_html.find('span', {'class': 'longitude'})

        if latitude_tag and longitude_tag:
            latitude = dms_to_decimal(latitude_tag.text)
            longitude = dms_to_decimal(longitude_tag.text)
            print(
                f"Klient: {client_name}, Lokalizacja: {client_location}, Szerokość geograficzna: {latitude}, Długość geograficzna: {longitude}")
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{client_name},\n{client_location}",
                icon=folium.Icon(color='red')
            ).add_to(map)
        else:
            print(f"Nie udało się znaleźć współrzędnych dla lokalizacji: {client_location}")

    map_dir = 'models/maps'
    os.makedirs(map_dir, exist_ok=True)

    map_file = os.path.join(map_dir, 'map_companies.html')
    map.save(map_file)
    webbrowser.open(map_file)