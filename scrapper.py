from json import loads
from urllib.parse import urlencode

from requests import get

from config import HEADERS, BASE_URL, HTML_URL
from tools import get_params_from_url, get_offers_count


def get_pages_count(offers_count, offers_per_page=40):
    pages_count = offers_count // offers_per_page
    return pages_count


def create_query(pagination, i):
    wants = {f"cat{i}": ["listResults"]}
    query = {
        'searchQueryState': pagination,
        'wants': str(wants),
        'requestId': '0',
    }
    return query


def parse_json(url, query):
    url = url + '?' + urlencode(query)
    responce = get(url.replace('+', ''), headers=HEADERS)
    return responce.text


def get_results():
    results = []
    offers_count = get_offers_count(HTML_URL)
    pages_count = get_pages_count(offers_count)
    pagination = get_params_from_url(HTML_URL)['searchQueryState'][0]
    pagination = loads(pagination)
    for i in (1, 2):
        for page in range(1, pages_count + 1):
            pagination['pagination']['currentPage'] = page
            query = create_query(pagination, i)
            result = parse_json(BASE_URL, query)
            results.append(result)
    print(f'{len(results)} pages parsed')
    return results, offers_count
