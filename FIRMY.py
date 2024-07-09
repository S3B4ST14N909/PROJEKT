from bs4 import BeautifulSoup
import requests
import folium
import webbrowser
import os


def get_coords(company_location):
    adres_url = f'https://pl.wikipedia.org/wiki/{company_location}'
    response = requests.get(adres_url)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    print([latitude, longitude])
    return [latitude, longitude]


def show_companies(companies):
    # Wyświetla listę firm
    print("Firmy tłumaczeniowe: ")
    for company in companies:
        print(f" {company['company_name']}")


def add_company(companies):
    # Dodaje nową firmę do listy
    company_name = input("Podaj nazwę firmy tłumaczeniowej do dodania: ")
    company_location = input("Podaj lokalizację firmy (miasto): ")
    companies.append({"company_name": company_name, "clients": [], "workers": [], "company_location": company_location})
    print(f" {company_name} został(a) pomyślnie dodana do listy.")
    show_companies(companies)


def remove_company(companies):
    # Usuwa firme z listy
    company_name = input("Podaj nazwę firmy do usunięcia: ")
    company_found = False
    for company in companies:
        if company['company_name'] == company_name:
            companies.remove(company)
            company_found = True
            print(f"{company_name} został(a) pomyślnie usunięta z listy.")
            break
    if not company_found:
        print(f"{company_name} nie znaleziono takiej firmy na liście.")
    show_companies(companies)


def update_company(companies):
    # Aktualizuje nazwę firmy
    old_company_name = input("Podaj nazwę firmy do aktualizacji: ")
    company_found = False
    for company in companies:
        if company['company_name'] == old_company_name:
            new_company_name = input(f"Podaj nową nazwę dla {old_company_name}: ")
            new_company_location = input(f"Podaj nową lokalizację firmy (miasto): ")
            company['company_name'] = new_company_name
            company['company_location'] = new_company_location
            company_found = True
            print(f"Nazwa firmy została zmieniona z {old_company_name} na {new_company_name}.")
            print(f"Lokalizacja firmy została zmieniona na {new_company_location}.")
            break
    if not company_found:
        print(f"{old_company_name} nie znaleziono takiej firmy na liście.")
    show_companies(companies)


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


def companies_map(companies):
    map = folium.Map(location=[52, 20], zoom_start=7)
    for company in companies:
        company_name = company['company_name']
        company_location = company['company_location']
        url = f"https://pl.wikipedia.org/wiki/{company_location}"

        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')

        latitude_tag = response_html.find('span', {'class': 'latitude'})
        longitude_tag = response_html.find('span', {'class': 'longitude'})

        if latitude_tag and longitude_tag:
            latitude = dms_to_decimal(latitude_tag.text)
            longitude = dms_to_decimal(longitude_tag.text)
            print(
                f"Firma: {company_name}, Lokalizacja: {company_location}, Szerokość geograficzna: {latitude}, Długość geograficzna: {longitude}")
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{company_name},\n{company_location}",
                icon=folium.Icon(color='red')
            ).add_to(map)
        else:
            print(f"Nie udało się znaleźć współrzędnych dla lokalizacji: {company_location}")

    map_dir = 'models/maps'
    os.makedirs(map_dir, exist_ok=True)

    map_file = os.path.join(map_dir, 'map_companies.html')
    map.save(map_file)
    webbrowser.open(map_file)

def language_search(companies: list[dict],) -> None:
    company_language = input("Podaj język na jaki chcesz przetłumaczyć:")
    for company in companies:
        if company_language == company['language']:
            print(f"firma która tłumaczy na ten język to: {company['company_name']}")




