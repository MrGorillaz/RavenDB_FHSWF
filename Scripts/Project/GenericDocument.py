import json

class GenericDocument:
    def __init__(self):
        self.__attributes__ = list()

    def addField(self, attribute, value):
        sub_object = ''
        sub_attribute = ''
        if "." in attribute:
            sub_object = attribute.split('.')[0]
            sub_attribute = attribute.split('.')[1]
        try:
            if sub_object:
                element = self.__attributes__.index(sub_object)
                getattr(self, self.__attributes__[element]).addField(sub_attribute, value)
            else:
                element = self.__attributes__.index(attribute)
                setattr(self, attribute, value)
        except ValueError:
            if sub_object:
                self.__attributes__.append(sub_object)
                sub_document = GenericDocument()
                sub_document.addField(sub_attribute, value)
                setattr(self, sub_object, sub_document)
            else:
                self.__attributes__.append(attribute)
                setattr(self, attribute, value)

    def __str__(self):
        output = '{'
        for attr in self.__attributes__:
            output = '{}"{}":"{}", '.format(output, attr, getattr(self, attr))
        output = "{}{}".format(output[:-2], '}')
        return output


class Shipper(GenericDocument):
    pass


class Customer(GenericDocument):

    def __init__(self):
        self.__attributes__ = list()
        self.__attributes__.append('Id')
        self.__attributes__.append('Name')
        self.__attributes__.append('Country')
        self.__attributes__.append('Geohash')
        self.__attributes__.append('Address')


class OrderItem(GenericDocument):
    pass


class Order(GenericDocument):
    def addField(self, attribute, value):
        self.__attributes__.append(attribute)
        # print("{} {}".format(attribute, value))
        if str(value).startswith('['):
            orders = json.loads(value)
            OrderItems = list()
            for order in orders:
                OrderItems.append(OrderItem())
                for key in order:
                    OrderItems[-1].addField(key, order[key])
            setattr(self, attribute, OrderItems)
        else:
            setattr(self, attribute, value)
