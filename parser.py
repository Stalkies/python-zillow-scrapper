from json import loads

from mysql import save_data
from scrapper import get_results

#result = result['cat1']['searchResults']['listResults'] if result['cat1']['searchResults']['listResults'] else []
def get_data(results):
    data = []
    i = 1
    for result in results:
        if i == 3:
            break
        result = loads(result)
        if f'cat{i}' in result:
            if result[f'cat{i}']['searchResults']['listResults']:
                result = result[f'cat{i}']['searchResults']['listResults']
                data.append(result)
                continue
        i += 1
    return data


def parse_data_to_list(data) -> list:
    results = []
    for i in data:
        for result in i:
            address = result['address'].split(',')[0] if result['address'] else None
            zpid = int(result['zpid']) if result['zpid'] else None
            city = result['addressCity'] if result['addressCity'] else None
            state = result['addressState'] if result['addressState'] else None
            zipcode = result['addressZipcode'] if result['addressZipcode'] else None
            price = result['unformattedPrice'] if result['unformattedPrice'] else None
            beds = result['beds'] if result['beds'] else None
            baths = result['baths'] if result['baths'] else None
            statusType = result['statusType'] if result['statusType'] else None
            statusText = result['statusText'] if result['statusText'] else None
            area = result['area'] if result['area'] else None
            isZillowOwned = result['isZillowOwned']
            detailUrl = result['detailUrl']
            if 'brokerName' in result:
                brokerName = result['brokerName'] if result['brokerName'] else None
            else:
                brokerName = None
            results.append(
                [zpid, address, city, state, zipcode, price, beds, baths, statusType, statusText, area, isZillowOwned,
                 brokerName, detailUrl])
    return results


def main():
    results, offers_count = get_results()
    data = get_data(results)
    results = parse_data_to_list(data)
    save_data(results)


if __name__ == '__main__':
    main()
