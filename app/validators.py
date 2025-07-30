import re

from werkzeug.datastructures import ImmutableMultiDict


class ContactValidator:
    def __init__(self, data: ImmutableMultiDict[str, str]):
        self.data: dict[str, str] = data.to_dict()
        self.errors: dict[str, str] = {}

    def validate_first_name(self):
        first_name = self.data.get('first_name', '')
        if not first_name:
            self.errors['first_name'] = 'Поле "Имя" обязательно для заполнения'
        elif not first_name[0].isupper():
            self.errors['first_name'] = (
                'Имя должно начинаться с заглавной буквы'
            )

    def validate_last_name(self):
        last_name = self.data.get('last_name', '')
        if last_name and not last_name[0].isupper():
            self.errors['last_name'] = (
                'Фамилия должна начинаться с заглавной буквы'
            )

    def validate_phone(self):
        phone = self.data.get('phone', '').strip()

        if phone:
            cleaned = re.sub(r'[ \-\(\)]', '', phone)

            if cleaned.startswith('+'):
                digits = cleaned[1:]
            else:
                digits = cleaned

            if not digits.isdigit():
                self.errors['phone'] = (
                    'Телефон должен содержать только цифры'
                    ' (после "+" разрешены пробелы, скобки и дефисы)'
                )

    def validate(self) -> dict[str, str]:
        self.validate_first_name()
        self.validate_last_name()
        self.validate_phone()
        return self.errors
