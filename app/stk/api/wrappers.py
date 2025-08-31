from app.data.repository import Contact
from app.stk.api.client import ApiClient


class ContactsApi(ApiClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def create(self, contact: Contact):
        payload = contact.to_dict()
        return self.post(
            endpoint='/contacts/',
            json_data=payload,
            check_schema=Contact,
        )
