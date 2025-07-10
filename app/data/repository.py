import random
import uuid
from dataclasses import dataclass
from datetime import date

from faker import Faker
from werkzeug.datastructures import ImmutableMultiDict

from app.common import str_to_date
from app.data.enums import Category, Channel, Gender, Priority

fake = Faker(locale='ru_RU')


@dataclass
class Contact:
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

    @classmethod
    def empty(cls) -> 'Contact':
        return cls(
            id=None,
            first_name=None,
            last_name=None,
            gender=None,
            phone=None,
            email=None,
            date_of_birth=None,
            priority=None,
            category=None,
            channels=None,
            current_address=None,
        )

    @classmethod
    def from_form_data(
        cls, form_data: ImmutableMultiDict[str, str]
    ) -> 'Contact':
        data = form_data.to_dict()
        channels_list = form_data.getlist('channels')

        gender: Gender = (
            Gender[data['gender']]
            if data.get('gender') in Gender.__members__
            else Gender.other
        )

        priority: Priority = (
            Priority[data['priority']]
            if data.get('priority') in Priority.__members__
            else Priority.regular
        )

        category: Category = (
            Category[data['category']]
            if data.get('category') in Category.__members__
            else Category.not_selected
        )

        channels: list[Channel] = []
        for value in channels_list:
            try:
                if value in Channel.__members__:
                    channels.append(Channel[value])
            except KeyError:
                continue

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


class ContactsRepository:
    _contacts: list[Contact]

    def __init__(self, contacts: list[Contact] | None = None) -> None:
        self._contacts = contacts or []

    def create(self, contact: Contact) -> None:
        if contact.id is None:
            contact.id = self._generate_id()
        self._contacts.append(contact)

    def read(self) -> list[Contact]:
        return self._contacts

    def update(
        self,
        id: str,
        first_name: str | None = None,
        last_name: str | None = None,
        gender: Gender | None = None,
        phone: str | None = None,
        email: str | None = None,
        date_of_birth: date | None = None,
        priority: Priority | None = None,
        category: Category | None = None,
        channels: list[Channel] | None = None,
        current_address: str | None = None,
    ) -> None:
        contact: Contact | None = self.find_by_id(id)

        if contact is not None:
            if first_name is not None:
                contact.first_name = first_name
            if last_name is not None:
                contact.last_name = last_name
            if gender is not None:
                contact.gender = Gender(gender)
            if phone is not None:
                contact.phone = phone
            if email is not None:
                contact.email = email
            if date_of_birth is not None:
                contact.date_of_birth = date_of_birth
            if priority is not None:
                contact.priority = Priority(priority)
            if category is not None:
                contact.category = Category(category)
            if channels is not None:
                contact.channels = channels
            if current_address is not None:
                contact.current_address = current_address
        else:
            return None

    def delete(self, id: str) -> None:
        contact: Contact | None = self.find_by_id(id)
        if contact:
            self._contacts.remove(contact)
        else:
            return None

    def find_by_id(self, id: str) -> Contact | None:
        for contact in self._contacts:
            if id == contact.id:
                return contact
        return None

    def find_by_name_or_last_name(self, query: str) -> list[Contact]:
        found_contacts: list[Contact] = []

        for contact in self._contacts:
            if (
                contact.first_name
                and query.lower() in contact.first_name.lower()
            ) or (
                contact.last_name
                and query.lower() in contact.last_name.lower()
            ):
                found_contacts.append(contact)

        return found_contacts

    def generate_contacts_data(self, count: int = 3) -> None:
        for _ in range(count):
            self.create(
                Contact(
                    ContactsRepository._generate_id(),
                    fake.first_name(),
                    fake.last_name(),
                    random.choice(list(Gender)),
                    fake.phone_number(),
                    fake.email(),
                    fake.date_of_birth(),
                    random.choice(list(Priority)),
                    random.choice(list(Category)),
                    random.sample(
                        list(Channel), k=random.randint(1, len(Channel))
                    ),
                    fake.street_address(),
                )
            )

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())[:4]
