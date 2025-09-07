import uuid

import pytest

from app.data.repository import Contact


@pytest.mark.smoke
def test_deleting_a_contact(contacts_api):
    contact = Contact.with_only_first_name()
    contact = contacts_api.create(contact)

    response = contacts_api.delete(contact.id)

    assert response.text == ''


@pytest.mark.extended
def test_deleting_a_nonexist_contact(contacts_api):
    response = contacts_api.delete(str(uuid.uuid4()))

    assert response.error == 'Contact not found'


pytestmark = pytest.mark.api
