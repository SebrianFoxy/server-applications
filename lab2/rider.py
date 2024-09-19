class Rider:
    def __init__(self, name):
        self.name = name
        self.equipment = []

    def add_equipment(self, equipment):
        self.equipment.append(equipment)

    def total_cost(self):
        return sum(item.price for item in self.equipment)

    def sort_by_weight(self):
        return sorted(self.equipment, key=lambda item: item.weight)

    def filter_by_price(self, min_price, max_price):
        return [item for item in self.equipment if min_price <= item.price <= max_price]
