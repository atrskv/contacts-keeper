import json
import logging
from json import JSONDecodeError

import allure
import requests
from requests import HTTPError, RequestException
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)

from app.common import is_json_serializable

logger = logging.getLogger('test')


class RequestFailureException(HTTPError, AssertionError):
    pass


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def _logging_pre(method, url, headers, data, files, expected_status):
        if data is not None and is_json_serializable(data):
            data = json.dumps(data, indent=4, ensure_ascii=False)

        if headers is not None and is_json_serializable(headers):
            headers = json.dumps(dict(headers), indent=4, ensure_ascii=False)

        text = (
            f'Performing {method} request:\n'
            f'url: {url}\n'
            f'headers: {headers}\n'
            f'data: {data}\n\n'
            f'files: {files}\n\n'
            f'expected status: {expected_status}\n\n'
        )

        allure.attach(
            text, 'request', attachment_type=allure.attachment_type.TEXT
        )

        logger.info(text)

    @staticmethod
    def _logging_post(response):
        try:
            data = json.dumps(response.json(), indent=4)
        except JSONDecodeError:
            data = response.text

        text = (
            'Got response:\n'
            f'response status: {response.status_code}\n'
            f'response content: {data}\n\n'
        )

        allure.attach(
            text, 'response', attachment_type=allure.attachment_type.TEXT
        )
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
        check_schema=None,
        check_status=True,
        expect_status=200,
        jsonify=True,
    ):
        url = self.base_url + location

        logger.info('-' * 100 + '\n')

        self._logging_pre(
            method, url, headers, data or json_data, files, expect_status
        )
        response = self.session.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            json=json_data,
            files=files,
        )

        self._logging_post(response)

        if check_status:
            response.raise_for_status()

        if expect_status and response.status_code != expect_status:
            raise RequestFailureException(
                f'Request {url} failed with [{response.status_code}]: {response.text}'
            )

        if jsonify:
            return response.json()

        return response

    def get(self, endpoint, expected_status=200, **kwargs):
        return self._request(
            'GET', endpoint, expect_status=expected_status, **kwargs
        )

    def post(self, endpoint, expected_status=201, **kwargs):
        return self._request(
            'POST', endpoint, expect_status=expected_status, **kwargs
        )

    def put(self, endpoint, expected_status=200, **kwargs):
        return self._request(
            'PUT', endpoint, expect_status=expected_status, **kwargs
        )

    def delete(self, endpoint, expected_status=204, **kwargs):
        return self._request(
            'DELETE', endpoint, expect_status=expected_status, **kwargs
        )
