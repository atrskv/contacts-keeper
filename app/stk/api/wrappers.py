from app.data.domains.models import Contact
from app.data.dto.contacts import (
    ContactResponse,
    ContactsErrorResponse,
    ContactsListResponse,
    ContactsValidationErrorResponse,
)
from app.stk.api.client import ApiClient


class ContactsApi(ApiClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def create(self, contact: Contact | None = None, **kwargs):
        if contact:
            payload = contact.to_dict()

            response = self._post(
                endpoint='/contacts/',
                json_data=payload,
                expected_schema=ContactResponse,
                expected_error_schema=ContactsValidationErrorResponse,
                **kwargs,
            )

            if isinstance(response, ContactsValidationErrorResponse):
                return response
            else:
                return response.to_domain_model()

        else:
            response = self._post(
                endpoint='/contacts/',
                json_data={},
                expected_schema=ContactResponse,
                expected_error_schema=ContactsErrorResponse,
                **kwargs,
            )

        return response

    def read(self, id, **kwargs):
        response = self._get(
            endpoint=f'/contacts/{id}',
            expected_schema=ContactResponse,
            expected_error_schema=ContactsErrorResponse,
            **kwargs,
        )

        if isinstance(response, ContactsErrorResponse):
            return response
        else:
            return response.to_domain_model()

    def read_random(self, **kwargs):
        response = self._get(
            endpoint='/contacts/random/',
            expected_schema=ContactResponse,
            expected_error_schema=ContactsErrorResponse,
            **kwargs,
        )

        if isinstance(response, ContactsErrorResponse):
            return response
        else:
            return response.to_domain_model()

    def read_list(self, page=1, query='', **kwargs):
        response = self._get(
            endpoint='/contacts/',
            params={'page': page, 'query': query},
            expected_schema=ContactsListResponse,
            expected_error_schema=ContactsErrorResponse,
            **kwargs,
        )

        if isinstance(response, ContactsErrorResponse):
            return response
        else:
            return response.to_domain_model()

    def update(self, id, new_data, **kwargs):
        response = self._put(
            endpoint=f'/contacts/{id}/',
            json_data=new_data.to_dict(),
            expected_schema=ContactResponse,
            expected_error_schema=ContactsValidationErrorResponse,
            **kwargs,
        )

        if isinstance(response, ContactsValidationErrorResponse):
            return response
        else:
            return response.to_domain_model()

    def delete(self, id, **kwargs):
        response = super()._delete(
            endpoint=f'/contacts/{id}/',
            expected_schema=None,
            expected_error_schema=ContactsErrorResponse,
            **kwargs,
        )

        return response
