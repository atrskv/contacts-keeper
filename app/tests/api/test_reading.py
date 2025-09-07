import uuid

import pytest

from app.data.domains.models import Contact


@pytest.mark.smoke
def test_reading_unique_contacts(contacts_api):
    for _ in range(10):
        contacts_api.create(Contact.with_random_data())

    response = contacts_api.read_list()
    ids = [contact.id for contact in response.contacts]

    assert response.page == 1
    assert len(ids) == len(set(ids))


@pytest.mark.smoke
def test_reading_a_random_contact(contacts_api):
    response = contacts_api.read_random()

    assert response.id is not None
    assert response.first_name is not None


@pytest.mark.critical_path
def test_reading_a_contact_by_id(contacts_api):
    contact = Contact.with_random_data()
    created_contact = contacts_api.create(contact)

    response = contacts_api.read(created_contact.id)

    assert response.id == created_contact.id
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
def test_reading_unique_contacts_from_second_page(contacts_api):
    for _ in range(20):
        contacts_api.create(Contact.with_random_data())

    response = contacts_api.read_list(page=2)
    ids = [contact.id for contact in response.contacts]

    assert response.page == 2
    assert len(ids) == len(set(ids))


@pytest.mark.extended
def test_reading_a_contact_by_invalid_id(contacts_api):
    random_string = str(uuid.uuid4())

    response = contacts_api.read(random_string)

    assert response.error == 'Contact not found'


class TestFindingContacts:
    @pytest.mark.smoke
    def test_finding_a_contact_by_last_name(self, contacts_api):
        contact = Contact.with_random_data()
        created_contact = contacts_api.create(contact)

        response = contacts_api.read_list(query=created_contact.last_name)
        finded_contact = response.contacts[0]

        assert response.page == 1
        assert response.pages == 1
        assert response.total == 1
        assert finded_contact.id == created_contact.id
        assert finded_contact.first_name == contact.first_name
        assert finded_contact.last_name == contact.last_name
        assert finded_contact.phone == contact.phone
        assert finded_contact.email == contact.email
        assert finded_contact.gender == contact.gender
        assert finded_contact.date_of_birth == contact.date_of_birth
        assert finded_contact.priority == contact.priority
        assert finded_contact.category == contact.category
        assert finded_contact.channels == contact.channels
        assert finded_contact.current_address == contact.current_address

    @pytest.mark.extended
    def test_finding_nonexistent_contact(self, contacts_api):
        random_string = str(uuid.uuid4())[:5]

        response = contacts_api.read_list(query=random_string)

        assert len(response.contacts) == 0
        assert response.page == 1
        assert response.pages == 0
        assert response.total == 0


pytestmark = pytest.mark.api
