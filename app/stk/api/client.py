import json
import logging
from json import JSONDecodeError
from typing import Any

import allure
import requests
from requests import RequestException
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)

from app.common import is_json_serializable

logger = logging.getLogger('test')


class UnexpectedStatusCodeException(Exception):
    pass


class ResponseValidationException(Exception):
    pass


class ApiClient:
    def __init__(self, host):
        self.host = host
        self.session = requests.Session()

    @staticmethod
    def _logging_pre(method, url, headers, data, files, expected_status_code):
        if data is not None and is_json_serializable(data):
            data = json.dumps(data, indent=4, ensure_ascii=False)

        if headers is not None:
            headers = dict(headers)
            if is_json_serializable(headers):
                headers = json.dumps(headers, indent=4, ensure_ascii=False)

        text = (
            f'method: {method}\n'
            f'url: {url}\n'
            f'headers: {headers}\n'
            f'data: {data}\n\n'
            f'files: {files}\n\n'
            f'expected status: {expected_status_code}\n\n'
        )

        allure.attach(text, 'request', allure.attachment_type.TEXT)
        logger.info(text)

    @staticmethod
    def _logging_post(response):
        try:
            data = json.dumps(response.json(), indent=4, ensure_ascii=False)
        except JSONDecodeError:
            data = response.text

        text = (
            f'response status: {response.status_code}\n'
            f'response data: {data}\n\n'
        )

        allure.attach(text, 'response', allure.attachment_type.TEXT)
        logger.info(text)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=(
            retry_if_exception_type(RequestException)
            | retry_if_result(
                lambda r: isinstance(r, requests.Response)
                and r.status_code in {502, 503, 504}
            )
        ),
        reraise=True,
    )
    def _request(
        self,
        method,
        location,
        headers=None,
        params=None,
        data=None,
        json_data=None,
        files=None,
        expected_status_code=None,
        expected_schema=None,
        expected_error_schema=None,
    ) -> Any:
        url = self.host + location

        logger.info('-' * 100 + '\n')

        payload = data if data is not None else json_data

        self._logging_pre(
            method, url, headers, payload, files, expected_status_code
        )

        try:
            response = self.session.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                files=files,
            )
        except RequestException as e:
            logger.error(f'Request failed: {e}')
            raise

        self._logging_post(response)

        # TODO: Create staticmethod valdiate()
        if (
            expected_status_code is not None
            and response.status_code != expected_status_code
        ):
            if 400 <= response.status_code < 600 and expected_error_schema:
                try:
                    response_data = response.json()
                    validated_error = expected_error_schema.model_validate(
                        response_data
                    )
                    return validated_error
                except (JSONDecodeError, ValueError) as e:
                    logger.error(f'Error validation failed: {e}')
                    raise ResponseValidationException(
                        f'Error response validation failed: {e}'
                    )

            error_msg = f'Unexpected status code [{response.status_code}], expected {expected_status_code}: {response.text}'

            logger.error(error_msg)

            raise UnexpectedStatusCodeException(error_msg)

        if 400 <= response.status_code < 600:
            if expected_error_schema:
                try:
                    response_data = response.json()
                    validated_error = expected_error_schema.model_validate(
                        response_data
                    )
                    return validated_error
                except (JSONDecodeError, ValueError) as e:
                    logger.error(f'Error validation failed: {e}')
                    raise ResponseValidationException(
                        f'Error response validation failed: {e}'
                    )

            return response

        if expected_schema:
            try:
                response_data = response.json()
                validated_response = expected_schema.model_validate(
                    response_data
                )
                return validated_response
            except (JSONDecodeError, ValueError, TypeError) as e:
                logger.error(f'Validation failed: {e}')
                logger.error(f'Response data: {response.text}')
                raise ResponseValidationException(
                    f'Error response validation failed: {e}'
                )

        return response

    def _get(
        self,
        endpoint,
        expected_status_code=200,
        expected_schema=None,
        expected_error_schema=None,
        **kwargs,
    ):
        return self._request(
            'GET',
            endpoint,
            expected_status_code=expected_status_code,
            expected_schema=expected_schema,
            expected_error_schema=expected_error_schema,
            **kwargs,
        )

    def _post(
        self,
        endpoint,
        expected_status_code=201,
        expected_schema=None,
        expected_error_schema=None,
        **kwargs,
    ):
        return self._request(
            'POST',
            endpoint,
            expected_status_code=expected_status_code,
            expected_schema=expected_schema,
            expected_error_schema=expected_error_schema,
            **kwargs,
        )

    def _put(
        self,
        endpoint,
        expected_status_code=200,
        expected_schema=None,
        expected_error_schema=None,
        **kwargs,
    ):
        return self._request(
            'POST',
            endpoint,
            expected_status_code=expected_status_code,
            expected_schema=expected_schema,
            expected_error_schema=expected_error_schema,
            **kwargs,
        )

    def _delete(
        self,
        endpoint,
        expected_status_code=204,
        expected_schema=None,
        expected_error_schema=None,
        **kwargs,
    ):
        return self._request(
            'DELETE',
            endpoint,
            expected_status_code=expected_status_code,
            expected_schema=expected_schema,
            expected_error_schema=expected_error_schema,
            **kwargs,
        )
