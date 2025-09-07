import random
from datetime import date

from faker import Faker
from pydantic import BaseModel

from app.common import date_to_str, str_to_date, unique_suffix
from app.data.domains.enums import Category, Channel, Gender, Priority

fake = Faker(locale='ru_RU')


class Contact(BaseModel):
    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: Gender | None = None
    phone: str | None = None
    email: str | None = None
    date_of_birth: date | None = None
    priority: Priority | None = None
    category: Category | None = None
    channels: list[Channel] | None = None
    current_address: str | None = None

    # TODO: Gender.other and etc -> None?
    @classmethod
    def with_only_first_name(cls) -> 'Contact':
        return cls(
            id=None,
            first_name=fake.first_name() + unique_suffix(),
            last_name=None,
            gender=Gender.other,
            phone=None,
            email=None,
            date_of_birth=None,
            priority=Priority.regular,
            category=Category.not_selected,
            channels=None,
            current_address=None,
        )

    @classmethod
    def with_random_data(cls) -> 'Contact':
        return cls(
            id=None,
            first_name=fake.first_name() + unique_suffix(),
            last_name=fake.last_name() + unique_suffix(),
            gender=random.choice(list(Gender)),
            phone=fake.phone_number(),
            email=fake.email(),
            date_of_birth=fake.date_of_birth(),
            priority=random.choice(list(Priority)),
            category=random.choice(list(Category)),
            channels=random.sample(
                list(Channel), k=random.randint(1, len(Channel))
            ),
            current_address=fake.street_address(),
        )

    @classmethod
    def from_json(cls, data: dict) -> 'Contact':
        channels_list = data.get('channels', [])

        gender_str = data.get('gender')
        if isinstance(gender_str, str) and gender_str in Gender.__members__:
            gender = Gender[gender_str]
        else:
            gender = Gender.other

        priority_str = data.get('priority')
        if (
            isinstance(priority_str, str)
            and priority_str in Priority.__members__
        ):
            priority = Priority[priority_str]
        else:
            priority = Priority.regular

        category_str = data.get('category')
        if (
            isinstance(category_str, str)
            and category_str in Category.__members__
        ):
            category = Category[category_str]
        else:
            category = Category.not_selected

        channels: list[Channel] = []
        for value in channels_list:
            if value in Channel.__members__:
                channels.append(Channel[value])

        return cls(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            gender=gender,
            phone=data.get('phone'),
            email=data.get('email'),
            date_of_birth=str_to_date(data.get('date_of_birth')),
            priority=priority,
            category=category,
            channels=channels,
            current_address=data.get('current_address'),
        )

    def to_model_with_enum_names(self, exclude: set = {'id'}) -> 'Contact':
        data = self.model_dump(exclude=exclude, mode='json')

        if self.gender is not None:
            data['gender'] = self.gender.name
        if self.priority is not None:
            data['priority'] = self.priority.name
        if self.category is not None:
            data['category'] = self.category.name
        if self.channels is not None:
            data['channels'] = [ch.name for ch in self.channels]

        return Contact.from_json(data)

    @classmethod
    def from_form_data(cls, form_data) -> 'Contact':
        channels_list = (
            form_data.getlist('channels')
            if hasattr(form_data, 'getlist')
            else form_data.get('channels', [])
        )
        if isinstance(channels_list, str):
            channels_list = [
                ch.strip() for ch in channels_list.split(',') if ch.strip()
            ]

        # TODO: Refactor
        gender = (
            Gender[form_data['gender']]
            if form_data.get('gender') in Gender.__members__
            else Gender.other
        )

        priority = (
            Priority[form_data['priority']]
            if form_data.get('priority') in Priority.__members__
            else Priority.regular
        )

        category = (
            Category[form_data['category']]
            if form_data.get('category') in Category.__members__
            else Category.not_selected
        )

        channels = [
            Channel[ch] for ch in channels_list if ch in Channel.__members__
        ]

        date_of_birth = None
        date_str = form_data.get('date_of_birth')

        if date_str:
            try:
                date_of_birth = str_to_date(date_str)
            except ValueError:
                date_of_birth = None

        return cls(
            first_name=form_data.get('first_name'),
            last_name=form_data.get('last_name'),
            gender=gender,
            phone=form_data.get('phone'),
            email=form_data.get('email'),
            date_of_birth=date_of_birth,
            priority=priority,
            category=category,
            channels=channels,
            current_address=form_data.get('current_address'),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender.name if self.gender else None,
            'phone': self.phone,
            'email': self.email,
            'date_of_birth': date_to_str(self.date_of_birth)
            if self.date_of_birth
            else None,
            'priority': self.priority.name if self.priority else None,
            'category': self.category.name if self.category else None,
            'channels': [ch.name for ch in self.channels]
            if self.channels
            else [],
            'current_address': self.current_address,
        }


class ContactsList(BaseModel):
    contacts: list[Contact]
    page: int
    pages: int
    total: int
