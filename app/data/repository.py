import random
import uuid
from dataclasses import dataclass
from datetime import date

from faker import Faker

from app.common import date_to_str, str_to_date, unique_suffix
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
    def random(cls) -> 'Contact':
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

        # TODO: Refactor
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


class ContactsRepository:
    def __init__(self, conn):
        self.conn = conn

    def create(self, contact: Contact) -> None:
        if contact.id is None:
            contact.id = self._generate_id()

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO contacts (
                        id, first_name, last_name, gender, phone,
                        email, date_of_birth, priority, category,
                        channels, current_address
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        contact.id,
                        contact.first_name,
                        contact.last_name,
                        contact.gender.name if contact.gender else None,
                        contact.phone,
                        contact.email,
                        contact.date_of_birth,
                        contact.priority.name if contact.priority else None,
                        contact.category.name if contact.category else None,
                        [ch.name for ch in contact.channels]
                        if contact.channels
                        else [],
                        contact.current_address,
                    ),
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())

    def read(self) -> list[Contact]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, last_name, gender, phone, email, date_of_birth,
                    priority, category, channels, current_address
                FROM contacts
            """)
            rows = cur.fetchall()

        contacts = []
        for row in rows:
            (
                id_,
                first_name,
                last_name,
                gender_str,
                phone,
                email,
                date_of_birth,
                priority_str,
                category_str,
                channels_list,
                current_address,
            ) = row

            channels = []
            if channels_list:
                for ch_str in channels_list:
                    try:
                        channels.append(Channel[ch_str])
                    except KeyError:
                        print(f"Warning: unknown channel '{ch_str}' in DB")

            contact = Contact(
                id=id_,
                first_name=first_name,
                last_name=last_name,
                gender=Gender[gender_str] if gender_str else None,
                phone=phone,
                email=email,
                date_of_birth=date_of_birth,
                priority=Priority[priority_str] if priority_str else None,
                category=Category[category_str] if category_str else None,
                channels=channels,
                current_address=current_address,
            )
            contacts.append(contact)

        return contacts

    # TODO:
    # Refactor update(self, id, first_name... -> update(self, contact: Contact)?

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
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE contacts
                    SET first_name = %s,
                        last_name = %s,
                        gender = %s,
                        phone = %s,
                        email = %s,
                        date_of_birth = %s,
                        priority = %s,
                        category = %s,
                        channels = %s,
                        current_address = %s
                    WHERE id = %s
                    """,
                    (
                        first_name,
                        last_name,
                        gender.name if gender else None,
                        phone,
                        email,
                        date_of_birth,
                        priority.name if priority else None,
                        category.name if category else None,
                        [ch.name for ch in channels] if channels else [],
                        current_address,
                        id,
                    ),
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def delete(self, id: str) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def find_by_id(self, id: str) -> Contact | None:
        contacts = self.read()
        for contact in contacts:
            if contact.id == id:
                return contact
        return None

    def find_by_name_or_last_name(self, query: str):
        contacts = self.read()
        found_contacts = []
        query_lower = query.strip().lower()

        for contact in contacts:
            first_name = (contact.first_name or '').strip().lower()
            last_name = (contact.last_name or '').strip().lower()

            if first_name.startswith(query_lower) or last_name.startswith(
                query_lower
            ):
                found_contacts.append(contact)

        return found_contacts

    def generate_contacts_data(self, count: int = 3) -> None:
        for _ in range(count):
            self.create(
                Contact(
                    id=ContactsRepository._generate_id(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
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
            )
