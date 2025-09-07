import re


class ContactValidator:
    def __init__(self, data: dict):
        self.data = data
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
        phone = (self.data.get('phone') or '').strip()

        if phone:
            cleaned = re.sub(r'[ \-\(\)]', '', phone)

            digits = cleaned[1:] if cleaned.startswith('+') else cleaned

            if not digits.isdigit():
                self.errors['phone'] = (
                    'Телефон должен содержать только цифры '
                    '(после "+" разрешены пробелы, скобки и дефисы)'
                )

    def validate(self) -> dict[str, str]:
        self.validate_first_name()
        self.validate_last_name()
        self.validate_phone()
        return self.errors
