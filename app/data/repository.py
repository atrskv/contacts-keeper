import uuid
from datetime import date

from app.data.domains.enums import Category, Channel, Gender, Priority
from app.data.domains.models import Contact


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
            self.create(Contact.with_random_data())
