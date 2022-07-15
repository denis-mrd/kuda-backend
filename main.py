import requests
import json
import yaml

with open('config.yml', 'r') as file:
    configuration = yaml.safe_load(file)

YANDEX_TOKEN = configuration['YANDEX_TOKEN']
AVIASALES_TOKEN = configuration['AVIASALES_TOKEN']
COUNTRIES = configuration['COUNTRIES']


def weather(latitude, longitude):
    # https://yandex.ru/dev/weather/doc/dg/concepts/forecast-info.html

    url = 'https://api.weather.yandex.ru/v2/informers'
    parameteres = {'lat': latitude, 'lon': longitude, 'lang': 'ru_RU'}
    apikey = {'X-Yandex-API-Key': YANDEX_TOKEN}
    request = requests.get(url, params=parameteres, headers=apikey)
    response = json.loads(request.text)
    return(response['fact']['feels_like'])


def airports(country):
    # https://support.travelpayouts.com/hc/ru/articles/360002322572-Aviasales-API-%D0%B0%D0%B2%D1%82%D0%BE%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B8%D1%82%D0%B0-%D0%B4%D0%BB%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD-%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2-%D0%B8-%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D0%BE%D0%B2
    
    url = 'http://autocomplete.travelpayouts.com/places2'
    parameteres = {'term': country, 'locale': 'ru', 'types[]': 'city'}
    request = requests.get(url, params=parameteres)
    response = json.loads(request.text)
    return(response)


def cheap_ticket(destination, departure_date):
    # https://support.travelpayouts.com/hc/ru/articles/203956163-Aviasales-API-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0-%D0%BA-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC-%D0%B4%D0%BB%D1%8F-%D1%83%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2-%D0%BF%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D1%81%D0%BA%D0%BE%D0%B9-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B

    url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
    parameteres = {'origin': 'MOW',
                   'destination': destination,
                   'currency': 'rub',
                   'departure_at': departure_date,
                   'sorting': 'price',
                   'direct': 'false',
                   'limit': '10',
                   'token': AVIASALES_TOKEN}
    request = requests.get(url, params=parameteres)
    response = json.loads(request.text)
    if response['success'] is True:
        ticket_list = response['data']
        for ticket in ticket_list:
            return print(f"Туда можно улететь из {ticket['origin']} ({ticket['origin_airport']}) по цене {ticket['price']} руб.")

    else:
        return(response['error'])


def search_country(country):
    for city in airports(country):
        print(
            f"Сейчас погода в {city['name']}: {weather(city['coordinates']['lat'], city['coordinates']['lon'])} по Цельсию")
        print(cheap_ticket(city['code'], '2022-07-14'))
        print('')


for country in COUNTRIES:
    search_country(country)

print('Done')
