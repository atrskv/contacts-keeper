import uuid
from dataclasses import dataclass
from datetime import date

from faker import Faker

from common import date_to_str, str_to_date

fake = Faker(locale='ru_RU')


@dataclass
class Contact:
    id: str

    name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    tags: list[str] | None = None
    date_of_birth: date | None = None
    current_address: str | None = None


class ContactsRepository:
    _contacts: list[Contact]

    def __init__(self, contacts: list[Contact] | None = None) -> None:
        self._contacts = contacts or []

    def create(
        self,
        name: str,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        tags: list[str] | None = None,
        date_of_birth: str | None = None,
        current_address: str | None = None,
    ) -> None:
        self._contacts.append(
            Contact(
                id=ContactsRepository._generate_id(),
                name=name,
                last_name=last_name,
                email=email,
                phone=phone,
                tags=tags,
                date_of_birth=str_to_date(date_of_birth),
                current_address=current_address,
            )
        )

    def read(self) -> list[Contact]:
        return self._contacts

    def update(
        self,
        id_: str,
        name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        tags: list[str] | None = None,
        date_of_birth: str | None = None,
        current_address: str | None = None,
    ) -> None:
        contact: Contact | None = self.find_by_id(id_)

        if contact:
            if name:
                contact.name = name
            if last_name:
                contact.last_name = last_name
            if email:
                contact.email = email
            if phone:
                contact.phone = phone
            if tags:
                contact.tags = tags
            if date_of_birth:
                contact.date_of_birth = str_to_date(date_of_birth)
            if current_address:
                contact.current_address = current_address

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

    def find_by_name_or_last_name(self, text: str) -> list[Contact]:
        found_contacts: list[Contact] = []

        for contact in self._contacts:
            if text in contact.name:
                found_contacts.append(contact)
            if contact.last_name is not None and text in contact.last_name:
                found_contacts.append(contact)

        return found_contacts

    def generate_contacts_data(self, count: int = 3) -> None:
        for _ in range(count):
            self.create(
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.phone_number(),
                fake.words(nb=3),
                date_to_str(fake.date_of_birth()),
                fake.street_address(),
            )

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())[:4]
