import requests
from config import HEADERS, BASE_URL, HTML_URL, pagination
from bs4 import BeautifulSoup
import json
from tools import encode_url, decode_url


def get_map_zoom(url):
    url = decode_url(url)
    index = url.find('mapZoom')
    map_zoom = url[index + 9: index + 9 + 2].replace(',', '').strip()
    return int(map_zoom)
def map_bounds_from_url(url):
    index = url.find('mapBounds')
    map_bounds = url[index + 15: index + 11 + 141]
    map_bounds = decode_url(map_bounds)
    map_bounds = map_bounds.replace(' ', '')
    map_bounds = map_bounds.replace('"', '')
    map_bounds = map_bounds.replace('{', '')
    map_bounds = map_bounds.replace('}', '')
    map_bounds = map_bounds.split(',')
    print(map_bounds)
    map_bounds = [float(i.split(':')[1]) for i in map_bounds]
    print(map_bounds)
    return map_bounds


def get_offers_count(url):
    responce = requests.get(url, headers=HEADERS)
    print(responce)
    soup = BeautifulSoup(responce.text, 'html.parser')
    offers_count = soup.find('button', {'class': 'option'}).find('div').text.replace(',', '')
    print(offers_count)
    return int(offers_count)

def get_pages_count(url, offers_count, offers_per_page=40):
    pages_count = offers_count // offers_per_page
    return pages_count if pages_count <= 20 else 20

def create_pagination(page: int, west, east, south, north) -> str:
    pagination['pagination']['currentPage'] = page
    pagination['mapBounds']['west'] = west
    pagination['mapBounds']['east'] = east
    pagination['mapBounds']['south'] = south
    pagination['mapBounds']['north'] = north
    pagination['mapZoom'] = get_map_zoom(HTML_URL)
    return pagination

def create_querry(pagination):
    query = {
        'searchQueryState': pagination,
        'wants': '{"cat1":["mapResults"]}',
        'requestId': '0',
    }
    return query



def parse_json(url, query):
    print(url+str(query)[2:-1])
    responce = requests.get(url+str(query)[2:-1], headers=HEADERS)
    print(responce.url)
    return responce.text



def get_results():
    offers_count = get_offers_count(HTML_URL)
    pages_count = get_pages_count(HTML_URL, offers_count)
    west, east, south, north = map_bounds_from_url(HTML_URL)
    results = []
    for i in range(1, pages_count+1):
        pagination = create_pagination(i, west, east, south, north)
        query = create_querry(str(pagination))
        json = parse_json(BASE_URL, query)
        results.append(json)
    return results
