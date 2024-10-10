class Phone:
    def __init__(self, id, surname, name, patronymic, address, credit_card, debit, credit, local_time, long_distance_time):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.address = address
        self.credit_card = credit_card
        self.debit = debit
        self.credit = credit
        self.local_time = local_time 
        self.long_distance_time = long_distance_time  

    def __repr__(self):
        return (f"{self.surname} {self.name} {self.patronymic},\n Адрес: {self.address},\n"
                f"Карта: {self.credit_card}, \n Дебет: {self.debit},\n Кредит: {self.credit},\n"
                f"Городские: {self.local_time} мин,\n Междугородные: {self.long_distance_time} мин")


subscribers = [
    Phone(1, "Иванов", "Иван", "Иванович", "ул. Ленина, 5", "1234567890123456", 5000, 2000, 30, 15),
    Phone(2, "Петров", "Петр", "Петрович", "ул. Победы, 10", "2345678901234567", 6000, 3000, 50, 0),
    Phone(3, "Сидоров", "Сидор", "Сидорович", "ул. Мира, 12", "3456789012345678", 7000, 4000, 70, 20),
]

def print_local_time_exceeds(time_limit):
    print(f"Абоненты с временем городских разговоров больше {time_limit} минут:")
    for subscriber in subscribers:
        if subscriber.local_time > time_limit:
            print(subscriber)
    print()

def print_long_distance_users():
    print("Абоненты, которые пользовались междугородной связью:")
    for subscriber in subscribers:
        if subscriber.long_distance_time > 0:
            print(subscriber)
    print()

def print_sorted_by_surname():
    print("Абоненты в алфавитном порядке по фамилии:")
    for subscriber in sorted(subscribers, key=lambda x: x.surname):
        print(subscriber)
    print()

print_local_time_exceeds(40)
print_long_distance_users()
print_sorted_by_surname()
