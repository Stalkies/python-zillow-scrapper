from scrapper import get_results
import json
from mysql import create_connection, create_table, insert_data, save_data


def get_data(results):
    data = []
    for result in results:
        result = json.loads(result)
        result = result['cat1']['searchResults']['listResults']
        data.append(result)
    return data


def parse_data_to_list(data) -> list:
    results = []
    for i in data:
        for result in i:
            address = result['address'] if result['address'] else None
            city = result['addressCity'] if result['addressCity'] else None
            state = result['addressState'] if result['addressState'] else None
            zipcode = result['addressZipcode'] if result['addressZipcode'] else None
            price = result['unformattedPrice'] if result['unformattedPrice'] else None
            beds = result['beds'] if result['beds'] else None
            baths = result['baths'] if result['baths'] else None
            results.append([address, city, state, zipcode, price, beds, baths])
    return results



def main():
    results = get_results()
    data = get_data(results)
    results = parse_data_to_list(data)
    save_data(results)

if __name__ == '__main__':
    main()