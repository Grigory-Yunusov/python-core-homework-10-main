from collections import UserDict
import re
from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def values(self, new_value):
        # Дополнительная логика в сеттере.
        self._value = new_value

    def __str__(self):
        return str(self._value)

    def validate(self):
        pass

class Name(Field):

    def __init__(self, name):
        super().__init__(name)


class Phone(Field):


    def __init__(self, phone):
        super().__init__(phone)
        # if not re.match(r'^\d{10}$', str(self._value)):
        #     raise ValueError("Phone must be a 100000000000000000-digit number.")

    def validate(self):
        if self._value and not (isinstance(self._value, str) and len(self._value) == 10 and self._value.isdigit()):
            raise ValueError("Phone must be a 10-digit number.")


    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Phone must be a string containing only digits.")
        self._value = new_value


class Birthday:
    def __init__(self, birthdate):
        self._value = None
        self.birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

    @Field.value.setter
    def value(self, new_value):
        
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format!!! Use YYYY-MM-DD.")

        self._value = new_value





class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None
    def add_phone(self, phone):
        phone_field = Phone(phone)
        phone_field.validate()
        self.phones.append(phone_field)

    def remove_phone(self, phone):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

        # self.phones = [p for p in self.phones if p.value != phone]

        # for p in self.phones:
        #     if p.value == phone:
        #         self.phones.remove(p)
        #         break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("not on the list!!")
        


    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        # return f"{phone} - not on the list!!!"
        return None

    def __str__(self):
        return f"Contact name: {self.name._value}, phones: {'; '.join(p.value for p in self.phones)}"


    def  days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.birthdate.month, self.birthday.birthdate.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.birthdate.month, self.birthday.birthdate.day).date()

            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        else:
            return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, term):

        if term in self.data:
            return self.data[term]
        else:
            return None
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __iter__(self):

        return iter(self.data.values())

    def iter_n_records(self, n):

        count = 0
        for record in self.data.values():
            yield record
            count += 1
            if count >= n:
                break


# Пример использования
phone_field = Phone("123456789")
print(phone_field.value)  # Вывод значения через getter

# Попытка установить некорректное значение для номера телефона
try:
    phone_field.value = "987-654-321"  # Это не число, вызовет ValueError
except ValueError as e:
    print(e)

birthday_field = Birthday("1990-01-01")
print(birthday_field.value)  # Вывод значения через getter

# Попытка установить некорректное значение для дня рождения
try:
    birthday_field.value = "1990/01/01"  # Некорректный формат даты, вызовет ValueError
except ValueError as e:
    print(e)
