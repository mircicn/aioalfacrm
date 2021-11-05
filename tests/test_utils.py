import json

import pytest

from aioalfacrm.core.exceptions import ApiException
from aioalfacrm.core.utils import make_url, check_response


@pytest.mark.parametrize(
    'hostname, api_method, branch_id, result',
    [
        ('demo.s20.online', 'branches', None, 'https://demo.s20.online/v2api/branches'),
        ('demo.test', 'customers', 1, 'https://demo.test/v2api/1/customers'),
        (None, None, None, 'https://None/v2api/None'),
    ]
)
def test_make_url(hostname: str, api_method: str, branch_id: int, result: str):
    url = make_url(hostname, api_method, branch_id)
    assert url == result


def test_check_response():
    json_response = check_response(200, json.dumps({"items": [{"name": "record"}]}))
    assert json_response == {"items": [{"name": "record"}]}


def test_not_json_response():
    with pytest.raises(ApiException) as exc:
        json_response = check_response(404, 'Not found')

    assert exc.value._message == 'Not found'
    assert exc.value._code == 404


def test_check_error_response():
    with pytest.raises(ApiException) as exc:
        check_response(500, 'Server error')
    assert exc.value._message == 'Server error'
    assert exc.value._code == 500


def test_check_bad_request_response():
    with pytest.raises(ApiException) as exc:
        check_response(400, json.dumps({"errors": ["First error"]}))
    assert exc.value._message == ["First error"]
    assert exc.value._code == 400
