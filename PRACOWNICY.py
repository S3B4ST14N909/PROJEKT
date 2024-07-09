from bs4 import BeautifulSoup
import requests
import folium
import webbrowser
import os
from Dane_osobowe import companies

def get_coords(worker_location):
    adres_url = f'https://pl.wikipedia.org/wiki/{worker_location}'
    response = requests.get(adres_url)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    print([latitude, longitude])
    return [latitude, longitude]


def show_workers(workers):
    # Wyświetla listę pracowników firmy
    company_name = input("Podaj nazwę kliniki, której lista pracowników ma zostać wyświetlona: ")
    company_found = False

    # Sprawdzenie, czy firma istnieje wśród pracowników
    for worker in workers:
        if worker['worker_company'] == company_name:
            company_found = True
            break

    # Wyświetlenie listy pracowników, jeśli firma została znaleziona
    if company_found:
        print(f"Lista pracowników kliniki {company_name}:")
        for worker in workers:
            if worker['worker_company'] == company_name:
                print(f" - {worker['worker_name']}")
    else:
        print(f"{company_name} nie znaleziono takiej kliniki na liście.")


def add_worker(workers, companies):
    # Dodaje nowego pracownika do firmy
    company_name = input("Podaj nazwę kliniki, do której chcesz dodać pracownika: ")
    company_found = False
    for company in companies:
        if company["company_name"] == company_name:
            worker_name = input(f"Podaj imię i nazwisko pracownika do dodania do {company_name}: ")
            worker_location = input(f"Podaj lokalizację pracownika (miasto): ")
            workers.append({
                "worker_name": worker_name,
                "worker_company": company_name,
                "worker_location": worker_location,

            })
            print(f"{worker_name} został(a) dodany(a) do listy pracowników kliniki {company_name}.")
            company_found = True
            break
    if not company_found:
        print(f"{company_name} nie znaleziono takiej kliniki na liście.")


def remove_worker(workers, comapnies):
    # Pobierz nazwę firmy i imię i nazwisko pracownika do usunięcia
    company_name = input("Podaj nazwę kliniki, z której chcesz usunąć pracownika: ")
    worker_name = input("Podaj imię i nazwisko pracownika do usunięcia: ")

    company_found = False
    worker_found = False

    # Sprawdzenie, czy firma istnieje
    for company in companies:
        if company['company_name'] == company_name:
            company_found = True
            break

    if not company_found:
        print(f"Nie znaleziono kliniki o nazwie {company_name}.")
        return

    # Usunięcie pracownika z podanej firmy
    for worker in workers:
        if worker['worker_name'] == worker_name and worker['worker_company'] == company_name:
            workers.remove(worker)
            worker_found = True
            print(f"Pracownik {worker_name} został usunięty z kliniki {company_name}.")
            break

    if not worker_found:
        print(f"Nie znaleziono pracownika o imieniu i nazwisku {worker_name} w klinice {company_name}.")


def update_worker(workers,companies):
    # Pobierz nazwę firmy i imię i nazwisko pracownika do aktualizacji
    company_name = input("Podaj nazwę kliniki, w której chcesz zaktualizować dane pracownika: ")
    worker_name = input("Podaj imię i nazwisko pracownika do zaktualizowania: ")

    company_found = False
    worker_found = False

    # Sprawdzenie, czy firmy istnieje
    for company in companies:
        if company['company_name'] == company_name:
            company_found = True
            break

    if not company_found:
        print(f"Nie znaleziono kliniki o nazwie {company_name}.")
        return

    # Aktualizacja danych pracownika
    for worker in workers:
        if worker['worker_name'] == worker_name and worker['worker_company'] == company_name:
            worker_found = True
            new_worker_name = input("Podaj nowe imię i nazwisko pracownika: ")
            new_worker_location = input("Podaj nową lokalizację pracownika: ")

            worker['worker_name'] = new_worker_name
            worker['worker_location'] = new_worker_location

            print(
                f"Zaktualizowano dane pracownika {worker_name} na {new_worker_name}, lokalizacja: {new_worker_location}.")
            break

    if not worker_found:
        print(f"Nie znaleziono pracownika o imieniu i nazwisku {worker_name} w klinice {company_name}.")


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


def workers_map(workers):
    map = folium.Map(location=[52, 20], zoom_start=7)

    for worker in workers:
        worker_name = worker['worker_name']
        worker_location = worker['worker_location']
        url = f"https://pl.wikipedia.org/wiki/{worker_location}"

        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')

        latitude_tag = response_html.find('span', {'class': 'latitude'})
        longitude_tag = response_html.find('span', {'class': 'longitude'})

        if latitude_tag and longitude_tag:
            latitude = dms_to_decimal(latitude_tag.text)
            longitude = dms_to_decimal(longitude_tag.text)
            print(
                f"Pracownik: {worker_name}, Lokalizacja: {worker_location}, Szerokość geograficzna: {latitude}, Długość geograficzna: {longitude}")
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{worker_name},\n{worker_location}",
                icon=folium.Icon(color='red'),
                tooltip=worker_name
            ).add_to(map)
        else:
            print(f"Nie udało się znaleźć współrzędnych dla lokalizacji: {worker_location}")

    map_dir = 'models/maps'
    os.makedirs(map_dir, exist_ok=True)

    map_file = os.path.join(map_dir, 'map_companies.html')
    map.save(map_file)
    webbrowser.open(map_file)


