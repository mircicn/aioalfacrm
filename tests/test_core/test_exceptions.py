from aioalfacrm.core.exceptions import AlfaException, ApiException


def test_init_alfa_exception():
    exception = AlfaException(
        code=402,
        message='Exception message',
    )

    assert exception._code == 402
    assert exception._message == 'Exception message'

    assert str(exception) == f'Code: 402 - Exception message'


def test_init_api_exception():
    exception = ApiException(
        code=402,
        message='Exception message',
        request_info='Fake request info',  # noqa
    )

    assert exception._code == 402
    assert exception._message == 'Exception message'
    assert exception._request_info == 'Fake request info'

    assert str(exception) == f'Code: 402 - Exception message Fake request info'
