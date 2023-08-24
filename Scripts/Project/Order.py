class OrderItem:
    def __init__(self, product: dict = None, quantity: int = 0, discount: int = 0):
        self.Product = product
        self.Quantity = quantity
        self.Discount = discount
        self.__attributes__ = list()
        self.__attributes__.append('Product')
        self.__attributes__.append('Quantity')
        self.__attributes__.append('Discount')

    def __str__(self):
        output = '{'
        output = '{}"Product":"{}", "Quantity":{}, "Discount":{}'.format(output, self.Product, self.Quantity, self.Discount)
        output = "{}{}".format(output, '}')
        return output


class Order:
    orderCount: int = 0

    def __init__(self, customer: str = None, timestamp: int = None, ordered: list[OrderItem] = None, shipwith: str = None):
        self.Id = "Orders/o-{:0>2d}".format(Order.orderCount+1)
        self.Customer = customer
        self.Timestamp = timestamp
        self.Ordered = ordered
        self.Shipwith = shipwith
        self.Collection = "Orders"
        self.__attributes__ = list()
        self.__attributes__.append('Id')
        self.__attributes__.append('Customer')
        self.__attributes__.append('Timestamp')
        self.__attributes__.append('Ordered')
        self.__attributes__.append('Shipwith')
        self.__attributes__.append('Collection')

        Order.orderCount += 1

    def __str__(self):
        output = '{'
        for attr in self.__attributes__:
            if isinstance(getattr(self, attr), list):
                output = "{}[".format(output)
                for item in getattr(self, attr):
                    output = "{}{}, ".format(output, item)
                output = "{}{}".format(output[:-2], ']')
            else:
                output = '{}"{}":"{}", '.format(output, attr, getattr(self, attr))
        output = "{}{}".format(output[:-2], '}')
        return output

    def getOrderedString(self):
        output = "["
        for item in self.Ordered:
            output = "{}{}, ".format(output, item)
        output = "{}{}".format(output[:-2], ']')
        return output