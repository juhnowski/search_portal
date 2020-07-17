import pytest
import requests
import schemathesis
from hypothesis import settings

from requests.auth import HTTPBasicAuth

BASE_URL = 'http://127.0.0.1:8000/api/v1'
schema = schemathesis.from_path('api_schemas/API-schema-users.json')


@pytest.fixture
def session():
    with requests.Session() as s:
        data = {"email": "admin@gmail.com", "password": "admin123"}
        auth_response = s.post(f'{BASE_URL}/login', data=data)
        token = auth_response.json()['token']
        s.headers['Authorization'] = f'Token {token}'
        yield s


@settings(max_examples=1)
@schema.parametrize()
def test_no_server_errors(case, session):
    print (session.headers)
    response = requests.request(
        case.method,
        f'{BASE_URL}{case.formatted_path}',
        headers=session.headers,
        params=case.query,
        json=case.body
    )
    assert response.status_code < 500
