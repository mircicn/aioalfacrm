import aiohttp
import pytest

from aioalfacrm import crud_objects
from aioalfacrm import models
from aioalfacrm.core import AuthManager, ApiClient
from . import add_auth_request

LOCATION_RESPONSE = {
    'page': 0,
    'total': 1,
    'count': 1,
    'items': [
        {
            'id': 1,
            'branch_id': 2,
            'name': 'Name',
            'is_active': 1,
            'weight': 0
        },
    ]
}


@pytest.fixture
def auth_manager():
    session = aiohttp.ClientSession()
    yield AuthManager(
        email='test@test.test',
        api_key='api-key',
        hostname='demo.s20.online',
        session=session,
    )


@pytest.fixture
def api_client(auth_manager: AuthManager):
    yield ApiClient(
        hostname='demo.s20.online',
        branch_id=1,
        auth_manager=auth_manager,
        session=auth_manager._session,  # noqa
    )


@pytest.mark.asyncio
async def test_location(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/location/index', 'POST', LOCATION_RESPONSE)

    location_object = crud_objects.Location(
        api_client=api_client,
        model_class=models.Location,
    )

    locations = await location_object.list()

    assert len(locations) == 1

    location = locations[0]

    assert location.id == 1
    assert location.branch_id == 2
    assert location.name == 'Name'
    assert location.is_active is True
    assert location.weight == 0
