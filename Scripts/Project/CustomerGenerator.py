import getopt
import sys
import random
import requests as req
import pygeohash as pgh
import pandas as pd


class CustomerGenerator:
    location_default = [46, 54, 3, 18]
    location_berlin = [52.35, 52.7, 13, 14]
    location_frankfurt = [50.5, 51.0, 7.6, 8.5]
    location_hamburg = [53.2, 53.8, 9.5, 10.5]
    location_list = [location_default, location_berlin, location_hamburg, location_frankfurt]

    def __init__(self, c_count: int, h_count: int):
        self.__customer_count__ = c_count
        self.__hotspot_count__ = h_count
        self.__customer__ = list()
        self.__company__names__ = self.__create_company_name_list__()

    def __create_osm_ids__(self, number: int, location: list) -> set:
        url = 'https://nominatim.openstreetmap.org/reverse?accept-language=de'
        params = dict(
            format='jsonv2',
            addressdetails='1'
        )
        ids = set()
        i = 0
        while i < number:
            params['lat'] = random.randint(int(location[0]) * 100000000000000,
                                           int(location[1]) * 100000000000000) / 100000000000000
            params['lon'] = random.randint(int(location[2]) * 100000000000000,
                                           int(location[3]) * 100000000000000) / 100000000000000
            try:
                osm_type = None
                resp = req.get(url=url, params=params).json()
                if resp['osm_type'] == 'node':
                    osm_type = 'N'
                elif resp['osm_type'] == 'way':
                    osm_type = 'W'
                elif resp['osm_type'] == 'relation':
                    osm_type = 'R'
                ids.add("{0}{1}".format(osm_type, str(resp['osm_id'])))
                i = i + 1
            except KeyError:
                continue
        return ids

    def __fetch_item_data_from_osm__(self, osm_ids: set) -> list:
        osm_ids_string = ''
        geo_items = list()
        params = dict(
            osm_ids='',
            format='jsonv2'
        )
        url = 'https://nominatim.openstreetmap.org/lookup?accept-language=de'
        while len(osm_ids) > 0:
            if len(osm_ids) > 50:
                count = 50
            else:
                count = len(osm_ids)
            for x in range(count):
                osm_ids_string = "{},{}".format(osm_ids_string, osm_ids.pop())
            params['osm_ids'] = osm_ids_string
            geo_item_request = req.get(url=url, params=params).json()
            geo_items = geo_items + geo_item_request
        return geo_items

    def __remove_incomplete_items__(self, geo_items: list) -> list:
        new_list = list()
        for item in geo_items:
            if ['road', 'postcode', 'village', 'house_number'] - item['address'].keys():
                continue
            new_list.append(item)
        return new_list

    def __enrich_with_geohash__(self, geo_items: list) -> list:
        for item in geo_items:
            geohash = pgh.encode(float(item['lat']), float(item['lon']))
            item['geohash'] = geohash
        return geo_items

    def __enrich_with_company_names__(self, geo_items: list) -> list:
        for item in geo_items:
            item['name'] = self.__company__names__.pop()
        return geo_items

    def __create_company_name_list__(self) -> set:
        wordlist_file = open("assets/cwordlist.txt", "r")
        words = wordlist_file.readlines()
        wordbook_size = len(words)
        company_names = set()
        for x in range(self.__customer_count__ + 100):
            company_names.add(str("{0} {1}".format(words[random.randint(0, wordbook_size - 1)].strip().capitalize(),
                                                   str(words[random.randint(0, wordbook_size - 1)].strip()))))
        return company_names

    def __export_to_csv__(self, geo_items: list):
        export = list()
        count = 1
        for item in geo_items:
            export.append({'Id': "customer/c-{0}".format(str(count).zfill(2)), 'Name': item['name'],
                           'Country': str(item['address']['country_code']).upper(), 'Geohash': item['geohash'],
                           'Address.Street': "{0} {1}".format(item['address']['road'],
                                                              item['address']['house_number']),
                           'Address.ZIPCode': item['address']['postcode'],
                           'Address.Town': item['address']['village'], '@metadata.@collection': 'Customer',
                           '@metadata.@id': "customer/c-{0}".format(str(count).zfill(2))})
            count = count + 1
        dataframe = pd.DataFrame(export)
        dataframe.to_csv('Customer.csv', index=False)

    def start(self):
        geo_items_sum = list()
        while len(geo_items_sum) < self.__customer_count__ * (1 - self.__hotspot_count__ * 0.2):
            print("....Generating Customer in default geo range")
            osm_ids = self.__create_osm_ids__(self.__customer_count__, type(self).location_list[0])
            geo_items = self.__fetch_item_data_from_osm__(osm_ids)
            geo_items = self.__remove_incomplete_items__(geo_items)
            print("Items created: {} this turn, {} over all".format(len(geo_items), len(geo_items)+len(geo_items_sum)))
            geo_items_sum = geo_items_sum + geo_items

        for i in range(1, self.__hotspot_count__):
            while len(geo_items_sum) < self.__customer_count__ * ((1 - self.__hotspot_count__ * 0.2) + 0.2 * i):
                print("....Generating Customer in hotspot {}".format(i))
                osm_ids = self.__create_osm_ids__(self.__customer_count__, type(self).location_list[0])
                geo_items = self.__fetch_item_data_from_osm__(osm_ids)
                geo_items = self.__remove_incomplete_items__(geo_items)
                print("Items created: {} this turn, {} over all".format(len(geo_items), len(geo_items) + len(geo_items_sum)))
                geo_items_sum = geo_items_sum + geo_items

        print(self.__customer_count__)
        print(self.__hotspot_count__)
        geo_items_sum = self.__enrich_with_geohash__(geo_items_sum)
        geo_items_sum = self.__enrich_with_company_names__(geo_items_sum)
        self.__export_to_csv__(geo_items_sum)


def main(argv):
    customer_count = 0
    hotspot_count = 0
    opts, args = getopt.getopt(argv, "hc:s:", ["customers=", "hotspots="])
    for opt, arg in opts:
        if opt == '-h':
            print('CustomerGenerator.py -c <customers> -s <hotspots>(0-3)')
            sys.exit()
        elif opt in ("-c", "--customers"):
            customer_count = arg
        elif opt in ("-s", "--hotspots"):
            hotspot_count = arg
        else:
            print('CustomerGenerator.py -c <customers> -s <hotspots>(0-3)')
            sys.exit()
    generator = CustomerGenerator(int(customer_count), int(hotspot_count))
    generator.start()


if __name__ == '__main__':
    main(sys.argv[1:])
