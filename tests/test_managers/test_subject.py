import aiohttp
import pytest

from aioalfacrm import entities
from aioalfacrm import managers
from aioalfacrm.core import AuthManager, ApiClient
from . import add_auth_request

SUBJECT_RESPONSE = {
    'page': 0,
    'total': 1,
    'count': 1,
    'items': [
        {
            'id': 1,
            'name': 'Name',
            'weight': 4,
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
async def test_subject(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/subject/index', 'POST', SUBJECT_RESPONSE)

    subject_object = managers.Subject(
        api_client=api_client,
        entity_class=entities.Subject,
    )

    subjects = await subject_object.list()

    assert len(subjects) == 1

    subject = subjects[0]

    assert subject.id == 1
    assert subject.name == 'Name'
    assert subject.weight == 4
