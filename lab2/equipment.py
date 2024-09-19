class Equipment:
    def __init__(self, name, price, weight):
        self._name = name
        self._price = price
        self._weight = weight

    def __str__(self):
        return f'{self._name}: Цена - {self._price}, Вес - {self._weight} кг'

    @property
    def price(self):
        return self._price

    @property
    def weight(self):
        return self._weight


class Helmet(Equipment):
    def __init__(self, name, price, weight, helmet_type):
        super().__init__(name, price, weight)
        self.helmet_type = helmet_type


class Jacket(Equipment):
    def __init__(self, name, price, weight, material):
        super().__init__(name, price, weight)
        self.material = material


class Gloves(Equipment):
    def __init__(self, name, price, weight, size):
        super().__init__(name, price, weight)
        self.size = size
