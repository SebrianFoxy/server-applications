import json
from equipment import Helmet, Jacket, Gloves
from rider import Rider


def load_equipment(file_path):
    with open(file_path, 'r') as file:
        equipment_data = json.load(file)

    equipment_list = []
    for item in equipment_data:
        if item['type'] == 'helmet':
            equipment_list.append(
                Helmet(item['name'], item['price'], item['weight'], item['helmet_type']))
        elif item['type'] == 'jacket':
            equipment_list.append(
                Jacket(item['name'], item['price'], item['weight'], item['material']))
        elif item['type'] == 'gloves':
            equipment_list.append(
                Gloves(item['name'], item['price'], item['weight'], item['size']))

    return equipment_list


def main():
    rider = Rider("Алексей")

    # Загрузка амуниции из файла
    equipment_list = load_equipment('lab2/data/equipment_data.json')

    # Экипировка мотоциклиста
    for item in equipment_list:
        rider.add_equipment(item)

    print(f"Общая стоимость амуниции: {rider.total_cost()} руб.")

    # Сортировка по весу
    sorted_equipment = rider.sort_by_weight()
    print("\nСортировка амуниции по весу:")
    for item in sorted_equipment:
        print(item)

    # Фильтрация по цене
    min_price = float(input("\nВведите минимальную цену: "))
    max_price = float(input("Введите максимальную цену: "))

    filtered_equipment = rider.filter_by_price(min_price, max_price)
    print(f"\nАмуниция в диапазоне цен от {min_price} до {max_price}:")
    for item in filtered_equipment:
        print(item)


if __name__ == "__main__":
    main()
