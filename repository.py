import random
import uuid
from dataclasses import dataclass
from datetime import date

from faker import Faker

fake = Faker(locale='ru_RU')


@dataclass
class Contact:
    id: str | None = None
    name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    email: str | None = None
    phone: str | None = None
    priority: str | None = None
    date_of_birth: date | None = None
    current_address: str | None = None
    notes: str | None = None


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
        name: str | None = None,
        last_name: str | None = None,
        gender: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        priority: str | None = None,
        date_of_birth: date | None = None,
        current_address: str | None = None,
        notes: str | None = None,
    ) -> None:
        contact: Contact | None = self.find_by_id(id)

        if contact is None:
            return None

        if name is not None:
            contact.name = name
        if last_name is not None:
            contact.last_name = last_name
        if gender is not None:
            contact.gender = gender
        if email is not None:
            contact.email = email
        if phone is not None:
            contact.phone = phone
        if priority is not None:
            contact.priority = priority
        if date_of_birth is not None:
            contact.date_of_birth = date_of_birth
        if current_address is not None:
            contact.current_address = current_address
        if notes is not None:
            contact.notes = notes

    def delete(self, id_: str) -> None:
        contact: Contact | None = self.find_by_id(id_)
        if contact:
            self._contacts.remove(contact)
        else:
            return None

    def find_by_id(self, id_: str) -> Contact | None:
        for contact in self._contacts:
            if id_ == contact.id:
                return contact
        return None

    def find_by_name_or_last_name(self, query: str) -> list[Contact]:
        found_contacts: list[Contact] = []

        for contact in self._contacts:
            if contact.name is not None and query in contact.name:
                found_contacts.append(contact)
            if contact.last_name is not None and query in contact.last_name:
                found_contacts.append(contact)

        return found_contacts

    def generate_contacts_data(self, count: int = 3) -> None:
        for _ in range(count):
            self.create(
                Contact(
                    ContactsRepository._generate_id(),
                    fake.first_name(),
                    fake.last_name(),
                    random.choice(['Мужчина', 'Женщина', '...']),
                    fake.email(),
                    fake.phone_number(),
                    random.choice(['Экстренной важности', 'Обычный']),
                    fake.date_of_birth(),
                    fake.street_address(),
                    fake.text(),
                )
            )

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())[:4]
