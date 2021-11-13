import aiohttp
import pytest

from aioalfacrm import entities
from aioalfacrm.core import AuthManager, ApiClient
from aioalfacrm.managers import Branch
from . import add_auth_request

BRANCH_RESPONSE = {
    'page': 0,
    'total': 1,
    'count': 1,
    'items': [
        {
            'id': 1,
            'name': 'name',
            'is_active': False,
            'subject_ids': [1, 2, 3],
            'weight': 1,
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
async def test_branch(aresponses, api_client):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/branch/index', 'POST', BRANCH_RESPONSE)
    branch_manager = Branch(
        api_client=api_client,
        entity_class=entities.Branch,

    )

    branches = await branch_manager.list()

    assert len(branches) == 1

    branch = branches[0]

    assert branch.id == 1
    assert branch.name == 'name'
    assert branch.is_active is False
    assert branch.subject_ids == [1, 2, 3]
    assert branch.weight == 1
