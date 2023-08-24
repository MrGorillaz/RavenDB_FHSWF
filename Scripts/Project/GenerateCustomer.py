import random
import pandas as pd
import pygeohash as pgh
import requests as req


def create_company_names():
    wordlist_file = open("assets/cwordlist.txt", "r")
    words = wordlist_file.readlines()
    wordbook_size = len(words)
    company_names = list()
    for x in range(50):
        company_names.append(str("{0} {1}".format(words[random.randint(0, wordbook_size - 1)].strip().capitalize(),
                                                  str(words[random.randint(0, wordbook_size - 1)].strip()))))
    return company_names


def create_osm_ids(lat_min: float = 46, lat_max: float = 54, lon_min: float = 3, lon_max: float = 18) -> list:
    url = 'https://nominatim.openstreetmap.org/reverse?accept-language=de'
    params = dict(
        format='jsonv2',
        addressdetails='1'
    )
    osm_ids = list()
    count = 50
    for x in range(count):
        params['lat'] = random.randint(int(lat_min) * 100000000000000, int(lat_max) * 100000000000000) / 100000000000000
        params['lon'] = random.randint(int(lon_min) * 100000000000000, int(lon_max) * 100000000000000) / 100000000000000
        try:
            osm_type = None
            resp = req.get(url=url, params=params).json()
            if resp['osm_type'] == 'node':
                osm_type = 'N'
            elif resp['osm_type'] == 'way':
                osm_type = 'W'
            elif resp['osm_type'] == 'relation':
                osm_type = 'R'
            osm_ids.append("{0}{1}".format(osm_type, str(resp['osm_id'])))
        except KeyError:
            x = x -1
            continue
    return osm_ids


def fetch_item_data(osm_ids: list = None):
    if len(osm_ids) > 1:
        osm_ids_string = ",".join(osm_ids)
    elif len(osm_ids) == 1:
        osm_ids_string = osm_ids.pop()
    else:
        return
    url = 'https://nominatim.openstreetmap.org/lookup?accept-language=de'
    params = dict(
        osm_ids=osm_ids_string,
        format='jsonv2'
    )
    geo_items = req.get(url=url, params=params).json()
    return geo_items


def delete_incomplete(items: list = None):
    new_list = list()
    for item in items:
        if ['road', 'postcode', 'village', 'house_number'] - item['address'].keys():
            continue
        new_list.append(item)
    return new_list


def enrich_with_geohash(items: list = None):
    for item in items:
        geohash = pgh.encode(float(item['lat']), float(item['lon']))
        item['geohash'] = geohash
    return items


def enrich_with_company_names(items: list = None):
    names = create_company_names()
    for x in range(len(items)):
        items[x]['name'] = names[x]
    return items


def export_to_csv(items: list = None):
    export = list()
    for x in range(len(items)):
        export.append({'Id': "customer/c-{0}".format(str(x + 1).zfill(2)), 'Name': items[x]['name'],
                       'Country': str(items[x]['address']['country_code']).upper(), 'Geohash': items[x]['geohash'],
                       'Address.Street': "{0} {1}".format(items[x]['address']['road'],
                                                          items[x]['address']['house_number']),
                       'Address.ZIPCode': items[x]['address']['postcode'],
                       'Address.Town': items[x]['address']['village'], '@metadata.@collection': 'Customer',
                       '@metadata.@id': "customer/c-{0}".format(str(x + 1).zfill(2))})
    dataframe = pd.DataFrame(export)
    dataframe.to_csv('Customer.csv', index=False)


# Generate Customer Data
def main_function(items: int = 0):
    geo_items_sum = list()
    print("This will take some time..... Get some coffee or do other stuff", flush=True)
    # Generate fully random addresses within operational borders (40%)
    while len(geo_items_sum) < items * 0.4:
        print("...........", flush=True)
        osm_ids = create_osm_ids()  # Default values => Central Europe
        geo_items = fetch_item_data(osm_ids)
        geo_items = delete_incomplete(geo_items)
        geo_items = enrich_with_geohash(geo_items)
        geo_items = enrich_with_company_names(geo_items)
        geo_items_sum += geo_items
        print(len(geo_items_sum), flush=True)
    ## Generate addresses within the area of Berlin (20%)
    while len(geo_items_sum) < items * 0.6:
        print("...........", flush=True)
        osm_ids = create_osm_ids(52.35, 52.7, 13, 14)  # Berlin
        geo_items = fetch_item_data(osm_ids)
        geo_items = delete_incomplete(geo_items)
        geo_items = enrich_with_geohash(geo_items)
        geo_items = enrich_with_company_names(geo_items)
        geo_items_sum += geo_items
        print(len(geo_items_sum), flush=True)
        ## Generate addresses within the area of Frankfurt (20%)
    while len(geo_items_sum) < items * 0.8:
        print("...........", flush=True)
        osm_ids = create_osm_ids(50.5, 51.0, 7.6, 8.5)  # Frankfurt
        geo_items = fetch_item_data(osm_ids)
        geo_items = delete_incomplete(geo_items)
        geo_items = enrich_with_geohash(geo_items)
        geo_items = enrich_with_company_names(geo_items)
        geo_items_sum += geo_items
        print(len(geo_items_sum), flush=True)
        ## Generate addresses within the area of Hamburg (20%)
    while len(geo_items_sum) < items:
        print("...........", flush=True)
        osm_ids = create_osm_ids(53.2, 53.8, 9.5, 10.5)
        geo_items = fetch_item_data(osm_ids)
        geo_items = delete_incomplete(geo_items)
        geo_items = enrich_with_geohash(geo_items)
        geo_items = enrich_with_company_names(geo_items)
        geo_items_sum += geo_items
        print(len(geo_items_sum), flush=True)
    export_to_csv(geo_items_sum[0:items])


if __name__ == '__main__':
    user_input = ''
    try:
        user_input = int(input('How many Customer do you need? : '))
    except ValueError:
        print("Not a number.")
    main_function(user_input)
