from werkzeug.datastructures import ImmutableMultiDict


class ContactValidator:
    def __init__(self, data: ImmutableMultiDict[str, str]) -> None:
        self.data: dict[str, str] = data.to_dict()
        self.errors: dict[str, str] = {}

    def validate_first_name(self) -> None:
        first_name: str = self.data.get('first_name', '')
        if not first_name:
            self.errors['first_name'] = 'Поле "Имя" обязательно для заполнения'
        elif not first_name[0].isupper():
            self.errors['first_name'] = (
                'Имя должно начинаться с заглавной буквы'
            )

    def validate_last_name(self) -> None:
        last_name: str = self.data.get('last_name', '')
        if last_name and not last_name[0].isupper():
            self.errors['last_name'] = (
                'Фамилия должна начинаться с заглавной буквы'
            )

    def validate_phone(self) -> None:
        phone = self.data.get('phone', '')

        if phone:
            if phone[0] == '+':
                digits = phone[1:]
            else:
                digits = phone

            if not digits.isdigit():
                self.errors['phone'] = 'Телефон должен содержать только цифры'

    def validate(self) -> dict[str, str]:
        self.validate_first_name()
        self.validate_last_name()
        self.validate_phone()
        return self.errors
