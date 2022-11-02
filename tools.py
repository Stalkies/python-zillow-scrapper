import urllib.parse
from sys import exit

from bs4 import BeautifulSoup
from requests import get

from config import HEADERS


def get_params_from_url(url: str) -> dict:
    params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    return params


def get_offers_count(url):
    responce = get(url, headers=HEADERS)
    if responce.status_code == 200:
        print('Successfull connection')
        soup = BeautifulSoup(responce.text, 'html.parser')
        agency_offers_count = soup.find('button', {'class': 'option'}).find('div').text.replace(',', '')
        other_offers_count = soup.find('button', {'class': 'option right-option'}).find('div').text.replace(',', '')
        offers_count = int(agency_offers_count) + int(other_offers_count)
        print(f'Agency offers count: {agency_offers_count}')
        print(f'Other offers count: {other_offers_count}')
        print(f'Offers count: {offers_count}')
        if int(agency_offers_count) == 0 and int(other_offers_count) == 0:
            print('No offers found')
            exit()
        if int(offers_count) > 800:
            print('Sorry, zillow.com has a limit of 800 offers per search. Please, try to narrow your search.')
            while True:
                answer = input('Do you want to parse only first 800 offers? (y/n): ')
                if answer == 'y':
                    return 800
                elif answer == 'n':
                    exit()
                else:
                    print('Please, enter y or n')

        return int(offers_count)
    print('Error, status code: ', responce.status_code, 'please, try again later')
    exit()
