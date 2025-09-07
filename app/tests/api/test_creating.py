import pytest

from app.data.repository import Contact


@pytest.mark.smoke
def test_creating_a_contact(contacts_api):
    contact = Contact.with_only_first_name()

    response = contacts_api.create(contact)

    assert response.id is not None
    assert response.first_name == contact.first_name
    assert response.last_name == contact.last_name
    assert response.phone == contact.phone
    assert response.email == contact.email
    assert response.gender == contact.gender
    assert response.date_of_birth == contact.date_of_birth
    assert response.priority == contact.priority
    assert response.category == contact.category
    assert response.channels == contact.channels
    assert response.current_address == contact.current_address


@pytest.mark.critical_path
def test_creating_a_contact_with_complete_random_data(contacts_api):
    contact = Contact.with_random_data()

    response = contacts_api.create(contact)

    assert response.id is not None
    assert response.first_name == contact.first_name
    assert response.last_name == contact.last_name
    assert response.phone == contact.phone
    assert response.email == contact.email
    assert response.gender == contact.gender
    assert response.date_of_birth == contact.date_of_birth
    assert response.priority == contact.priority
    assert response.category == contact.category
    assert response.channels == contact.channels
    assert response.current_address == contact.current_address


@pytest.mark.extended
class TestContactName:
    def test_creating_a_contact_with_lowercase_first_letter_in_first_name(
        self,
        contacts_api,
    ):
        contact = Contact.with_random_data()
        contact.first_name = (contact.first_name or '').lower()

        response = contacts_api.create(contact)

        assert len(response.errors) == 1
        assert (
            response.errors.first_name
            == 'Имя должно начинаться с заглавной буквы'
        )

    def test_creating_a_contact_with_lowercase_first_letter_in_last_name(
        self,
        contacts_api,
    ):
        contact = Contact.with_random_data()
        contact.last_name = (contact.last_name or '').lower()

        response = contacts_api.create(contact)

        assert len(response.errors) == 1
        assert (
            response.errors.last_name
            == 'Фамилия должна начинаться с заглавной буквы'
        )


@pytest.mark.extended
def test_creating_a_contact_with_letters_in_phone(
    contacts_api,
):
    contact = Contact.with_random_data()
    contact.phone = (contact.phone or '') + 'abc'

    response = contacts_api.create(contact)

    assert len(response.errors) == 1
    assert (
        response.errors.phone == 'Телефон должен содержать только цифры'
        ' (после "+" разрешены пробелы, скобки и дефисы)'
    )


@pytest.mark.extended
def test_creating_a_contact_with_empty_data(contacts_api):
    response = contacts_api.create()

    assert response.error == 'No JSON data provided'


pytestmark = pytest.mark.api
