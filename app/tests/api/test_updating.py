import pytest

from app.data.repository import Contact


@pytest.mark.smoke
def test_updating_a_contact(contacts_api):
    contact = Contact.with_only_first_name()
    contact = contacts_api.create(contact)
    new_data = Contact.with_random_data().to_model_with_enum_names()

    response = contacts_api.update(contact.id, new_data)

    assert response.id is not None
    assert response.first_name == new_data.first_name
    assert response.last_name == new_data.last_name
    assert response.phone == new_data.phone
    assert response.email == new_data.email
    assert response.gender == new_data.gender
    assert response.date_of_birth == new_data.date_of_birth
    assert response.priority == new_data.priority
    assert response.category == new_data.category
    assert response.channels == new_data.channels
    assert response.current_address == new_data.current_address


@pytest.mark.critical_path
def test_updating_a_contact_completely(contacts_api):
    contact = Contact.with_only_first_name()
    contact = contacts_api.create(contact)
    new_data = Contact.with_random_data().to_model_with_enum_names()

    response = contacts_api.update(contact.id, new_data)

    assert response.id is not None
    assert response.first_name == new_data.first_name
    assert response.last_name == new_data.last_name
    assert response.phone == new_data.phone
    assert response.email == new_data.email
    assert response.gender == new_data.gender
    assert response.date_of_birth == new_data.date_of_birth
    assert response.priority == new_data.priority
    assert response.category == new_data.category
    assert response.channels == new_data.channels
    assert response.current_address == new_data.current_address


@pytest.mark.extended
class TestContactName:
    def test_updating_a_contact_first_name_to_a_value_that_begins_with_a_lowercase_letter(
        self,
        contacts_api,
    ):
        contact = Contact.with_random_data()
        created_contact = contacts_api.create(contact)
        created_contact.first_name = (contact.first_name or '').lower()
        new_data = created_contact.to_model_with_enum_names()

        response = contacts_api.update(created_contact.id, new_data)

        assert len(response.errors) == 1
        assert (
            response.errors.first_name
            == 'Имя должно начинаться с заглавной буквы'
        )

    def test_updating_a_contact_last_name_to_a_value_that_begins_with_a_lowercase_letter(
        self,
        contacts_api,
    ):
        contact = Contact.with_random_data()
        created_contact = contacts_api.create(contact)
        created_contact.last_name = (contact.last_name or '').lower()
        new_data = created_contact.to_model_with_enum_names()

        response = contacts_api.update(created_contact.id, new_data)

        assert len(response.errors) == 1
        assert (
            response.errors.last_name
            == 'Фамилия должна начинаться с заглавной буквы'
        )


@pytest.mark.extended
def test_updating_a_contact_phone_to_a_value_that_contains_letters(
    contacts_api,
):
    contact = Contact.with_random_data()
    created_contact = contacts_api.create(contact)
    created_contact.phone = (contact.phone or '') + 'abc'
    new_data = created_contact.to_model_with_enum_names()

    response = contacts_api.update(created_contact.id, new_data)

    assert len(response.errors) == 1
    assert (
        response.errors.phone == 'Телефон должен содержать только цифры'
        ' (после "+" разрешены пробелы, скобки и дефисы)'
    )


pytestmark = pytest.mark.api
