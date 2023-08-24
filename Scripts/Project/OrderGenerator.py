import getopt
import sys
import random
import time
import pandas as pd
import requests as req

from Order import Order, OrderItem
from ravendb import DocumentStore


class OrderGenerator:
    highRatio = 0.35
    midRatio = 0.15
    lowRatio = 0.5
    highCount = 0
    midCount = 0
    lowCount = 0
    highRange = tuple([1514782800, 1577808000])
    midRange = tuple([1641013200, 1685570400])
    lowRange = tuple([1577854800, 1640966400])

    def __init__(self, remote, database):
        self.__remote__ = remote
        self.__database__ = database

        self.__customer_ids__ = list()
        self.__product_ids__ = list()
        self.__shipper_ids = list()

    def __init_database__(self):
        self.__store__ = DocumentStore(self.__remote__, self.__database__)
        self.__store__.initialize()
        self.__session__ = self.__store__.open_session()

    def __read_customers_from_db__(self):
        customer_ids = list()
        url = "{}/databases/{}/queries".format(self.__remote__, self.__database__)
        params = dict(
            Query='from Customers'
        )
        customer = req.get(url=url, params=params)
        for item in customer.json()['Results']:
            customer_ids.append(item['Id'])
        return customer_ids

    def __read_products_from_db__(self):
        product_ids = list()
        url = "{}/databases/{}/queries".format(self.__remote__, self.__database__)
        params = dict(
            Query='from Products'
        )
        products = req.get(url=url, params=params)
        for item in products.json()['Results']:
            product_ids.append(item['Id'])
        return product_ids

    def __read_shippers_from_db__(self):
        shipper_ids = list()
        url = "{}/databases/{}/queries".format(self.__remote__, self.__database__)
        params = dict(
            Query='from Shippers'
        )
        shippers = req.get(url=url, params=params)
        for item in shippers.json()['Results']:
            shipper_ids.append(item['Id'])
        return shipper_ids

    def __get_good_timestamp__(self):
        ranges = list()
        if OrderGenerator.lowCount < OrderGenerator.lowRatio * Order.orderCount:
            ranges.append(OrderGenerator.lowRange)
        if OrderGenerator.midCount < OrderGenerator.midRatio * Order.orderCount:
            ranges.append(OrderGenerator.midRange)
        if OrderGenerator.highCount < OrderGenerator.highRatio * Order.orderCount:
            ranges.append(OrderGenerator.highRange)
        trange = ranges[random.randint(0, len(ranges) - 1)]
        timestamp = random.randint(trange[0], trange[1])
        return timestamp

    def __create_order__(self, customer_id: str, product: list, shippers: list):
        order = Order()
        order.Timestamp = int(time.time())
        order.Customer = customer_id
        order.Shipwith = shippers[random.randint(0, len(shippers) - 1)]
        order.Ordered = list()
        order_set = set()
        for x in range(random.randint(1, len(product))):
            order_set.add(product[random.randint(0, len(product) - 1)])
        for item in order_set:
            order.Ordered.append(OrderItem(item, random.randint(1, 100), random.randint(0, 5)))
        return order

    def __export_to_csv__(self, orders):
        export = list()
        for order in orders:
            print(order)
            export.append({'Id': order.Id, 'Customer': order.Customer,
                           'Timestamp': order.Timestamp, 'Ordered': order.getOrderedString(),
                           'Shipwith': order.Shipwith, 'Collection': order.Collection,
                           '@metadata.@collection': 'Customer',
                           '@metadata.@id': order.Id})
        dataframe = pd.DataFrame(export)
        dataframe.to_csv('Orders.csv', index=False)

    def start(self):
        orders = list()
        self.__init_database__()
        customers = self.__read_customers_from_db__()
        products = self.__read_products_from_db__()
        shippers = self.__read_shippers_from_db__()
        for customer in customers:
            for x in range(random.randint(5, 100)):
                order = self.__create_order__(customer, products, shippers)
                order.Timestamp = self.__get_good_timestamp__()
                orders.append(order)
        self.__export_to_csv__(orders)


def main(argv):
    remote_path = ''
    database = ''
    opts, args = getopt.getopt(argv, "hr:d:", ["remotepath=", "database="])
    for opt, arg in opts:
        if opt == '-h':
            print('OrderGenerator.py -r <remote_server> -d <database>')
            sys.exit()
        elif opt in ("-r", "--remotepath"):
            remote_path = arg
        elif opt in ("-d", "--database"):
            database = arg
        else:
            print('OrderGenerator.py -r <remote_server> -d <database>')
            sys.exit()
    generator = OrderGenerator(remote_path, database)
    generator.start()


if __name__ == '__main__':
    main(sys.argv[1:])
