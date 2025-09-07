from pydantic import BaseModel

from app.common import str_to_date
from app.data.domains.enums import Category, Channel, Gender, Priority
from app.data.domains.models import ContactsList
from app.data.repository import Contact


class ContactResponse(BaseModel):
    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    phone: str | None = None
    email: str | None = None
    date_of_birth: str | None = None
    priority: str | None = None
    category: str | None = None
    channels: list[str] | None = None
    current_address: str | None = None

    def to_domain_model(self) -> Contact:
        return Contact(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=Gender[self.gender] if self.gender else None,
            phone=self.phone,
            email=self.email,
            date_of_birth=str_to_date(self.date_of_birth)
            if self.date_of_birth
            else None,
            priority=Priority[self.priority] if self.priority else None,
            category=Category[self.category] if self.category else None,
            channels=[Channel[ch] for ch in self.channels]
            if self.channels
            else None,
            current_address=self.current_address,
        )


class ContactsListResponse(BaseModel):
    contacts: list[ContactResponse]
    page: int
    pages: int
    total: int

    def to_domain_model(self) -> 'ContactsList':
        return ContactsList(
            contacts=[contact.to_domain_model() for contact in self.contacts],
            page=self.page,
            pages=self.pages,
            total=self.total,
        )


class ContactsErrorResponse(BaseModel):
    error: str


class ContactErrors(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

    def __len__(self):
        return sum(1 for v in self.__dict__.values() if v is not None)


class ContactsValidationErrorResponse(BaseModel):
    errors: ContactErrors
