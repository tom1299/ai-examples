class Customer:
    def __init__(self, email):
        self.email = email

class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Warehouse:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_product(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

class Order:
    def __init__(self, customer, product_name, quantity):
        self.customer = customer
        self.product_name = product_name
        self.quantity = quantity

class OnlineShop:
    def __init__(self):
        self.warehouse = Warehouse()

    def buy_product(self, order):
        product = self.warehouse.get_product(order.product_name)
        if product is None:
            return False
        if product.quantity < order.quantity:
            return False
        product.quantity -= order.quantity
        return True