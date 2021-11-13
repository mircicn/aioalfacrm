import aiohttp
import pytest

from aioalfacrm import crud_objects
from aioalfacrm import models
from aioalfacrm.core import AuthManager, ApiClient
from . import add_auth_request

LEAD_STATUS_RESPONSE = {
    'page': 0,
    'total': 1,
    'count': 1,
    'items': [
        {
            'id': 1,
            'name': 'Name',
            'is_enabled': 0,
            'weight': 2,
        }
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
async def test_lead_status(api_client, aresponses):
    add_auth_request(aresponses)

    aresponses.add('demo.s20.online', '/v2api/1/lead-status/index', 'POST', LEAD_STATUS_RESPONSE)

    lead_status_object = crud_objects.LeadStatus(
        api_client=api_client,
        model_class=models.LeadStatus
    )

    lead_statuses = await lead_status_object.list()

    assert len(lead_statuses) == 1

    lead_status = lead_statuses[0]

    assert lead_status.id == 1
    assert lead_status.name == 'Name'
    assert lead_status.is_enabled is False
    assert lead_status.weight == 2
