# Parent Class
class MenuItem:


    restaurant_name = "Food Mamy"

    def __init__(self, item_id, name, price, category, preparation_time):
        self.item_id = item_id
        self.name = name
        self.__price = price
        self.category = category
        self.preparation_time = preparation_time
        self.is_available = True

    def get_price(self):
        return self.__price

    def set_price(self, new_price):
        if new_price > 0:
            self.__price = new_price
        else:
            print("Invalid price")

    def set_availability(self, status):
        self.is_available = status

    def apply_discount(self, discount):
        if 0 < discount <= 100:
            self.__price -= self.__price * (discount / 100)
        else:
            print("Invalid discount")

    def display_item(self):
        return f"{self.name} - {self.get_price()} EGP"


# Subclasses
class MainDish(MenuItem):

    def __init__(self, item_id, name, price, category, preparation_time, portion_size):
        super().__init__(item_id, name, price, category, preparation_time)
        self.portion_size = portion_size


class Drink(MenuItem):

    def __init__(self, item_id, name, price, category, preparation_time, size):
        super().__init__(item_id, name, price, category, preparation_time)
        self.size = size


class Dessert(MenuItem):

    def __init__(self, item_id, name, price, category, preparation_time, sweetness_level):
        super().__init__(item_id, name, price, category, preparation_time)
        self.sweetness_level = sweetness_level


# Order Class
class Order:

    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.get_price()
        return total


# System Class
class RestaurantSystem:

    def __init__(self):
        self.menu = []

    def add_item(self, item):
        self.menu.append(item)

    def get_menu(self):
        return self.menu