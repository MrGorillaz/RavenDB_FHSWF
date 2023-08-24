import getopt

from ravendb import DocumentStore, QueryOperator
from GenericDocument import Customer, Order, Shipper

import sys
import pandas as pd


class DataImport:
    __documents__ = list()

    def __init__(self, input, remote, database, collection):
        self.__input__ = input
        self.__remote__ = remote
        self.__database__ = database
        self.__collection__ = collection

    def __init_database__(self):
        self.__store__ = DocumentStore(self.__remote__, self.__database__)
        self.__store__.initialize()
        self.__session__ = self.__store__.open_session()

    def __import_customer_csv__(self):
        df = pd.read_csv(self.__input__)
        attributes = df.columns
        for tup in df.itertuples():
            self.__documents__.append(Customer())
            for i in range(0, len(attributes)):
                self.__documents__[-1].addField(attributes[i], tup[i + 1])

    def __import_order_csv__(self):
        df = pd.read_csv(self.__input__)
        attributes = df.columns
        for tup in df.itertuples():
            self.__documents__.append(Order())
            for i in range(0, len(attributes)):
                self.__documents__[-1].addField(attributes[i], tup[i + 1])

    def __import_shipper_csv__(self):
        df = pd.read_csv(self.__input__)
        attributes = df.columns
        for tup in df.itertuples():
            self.__documents__.append(Shipper())
            for i in range(0, len(attributes)):
                self.__documents__[-1].addField(attributes[i], tup[i + 1])

    def __clear_collection__(self):
        query = self.__session__.query_collection(self.__collection__).wait_for_non_stale_results()
        results = list(query)
        for i in range(0, len(results)):
            self.__session__.delete(getattr(results[i], '@metadata')['@id'])
            print(getattr(results[i], '@metadata')['@id'])
        self.__session__.save_changes()

    def __push_to_database__(self):
        i = 0
        for document in self.__documents__:
            if i > 25:
                self.__session__.close()
                self.__session__ = self.__store__.open_session()
                i = 0
            print(getattr(document, 'Id'))
            self.__session__.store(document, getattr(document, 'Id'))
            self.__session__.save_changes()
            i += 1
        print("Done")

    def start(self):
        self.__init_database__()
        if self.__collection__ == "Customers":
            self.__import_customer_csv__()
        elif self.__collection__ == "Orders":
            self.__import_order_csv__()
        elif self.__collection__ == "Shippers":
            self.__import_shipper_csv__()
        else:
            exit(1)
        self.__clear_collection__()
        self.__push_to_database__()


def main(argv):
    input_file = ''
    remote_path = ''
    database = ''
    collection = ''
    opts, args = getopt.getopt(argv, "hi:r:d:c:", ["infile=", "remotepath=", "database=", "collection="])
    for opt, arg in opts:
        if opt == '-h':
            print('DataImport.py -i <inputfile> -r <remote_server> -d <database> -c <collection>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            input_file = arg
        elif opt in ("-r", "--remotepath"):
            remote_path = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("-c", "--collection"):
            collection = arg
        else:
            print('DataImport.py -i <inputfile> -r <remote_server> -d <database> -c <collection>')
            sys.exit()
    importer = DataImport(input_file, remote_path, database, collection)
    importer.start()


if __name__ == '__main__':
    main(sys.argv[1:])
