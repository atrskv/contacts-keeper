import os

import pytest
from dotenv import load_dotenv

from app.stk.api.client import ApiClient
from app.stk.api.wrappers import ContactsApi


@pytest.fixture(scope='session')
def load_env():
    load_dotenv('.env.test')


@pytest.fixture(scope='session')
def client(load_env):
    return ApiClient(os.getenv('API_URL'))


@pytest.fixture(scope='session')
def contacts_api(load_env):
    return ContactsApi(os.getenv('API_URL'))
