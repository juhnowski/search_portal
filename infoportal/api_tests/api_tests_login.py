import pytest
import requests
import schemathesis
from hypothesis import settings

from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000/api/v1"
schema = schemathesis.from_path('api_schemas/API-schema-login.json')


@settings(max_examples=2)
@schema.parametrize()
def test_no_server_errors(case):
    response = requests.request(
        case.method,
        f"{BASE_URL}{case.formatted_path}",
        headers=case.headers,
        params=case.query,
        json={"email": "admin@gmail.com", "password": "admin123"},
    )
    assert response.status_code < 500

