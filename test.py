from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Дополнительная логика в сеттере, если необходимо
        self._value = new_value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        # Логика валидации, если необходимо
        pass

    @Field.value.setter
    def value(self, new_value):
        # Проверка на корректность ведомого номера телефона
        if not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Phone must be a string containing only digits.")

        self._value = new_value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        # Проверка на корректность введенной даты рождения
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        self._value = new_value


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