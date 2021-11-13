import datetime

import aiohttp
import pytest

from aioalfacrm import entities
from aioalfacrm.core import AuthManager, ApiClient
from aioalfacrm.managers import CGI
from . import add_auth_request

CGI_RESPONSE = {
    'page': 0,
    'count': 1,
    'total': 1,
    'items': [
        {
            'id': 1,
            'customer_id': 5,
            'group_id': 3,
            'b_date': '01.01.2021',
            'e_date': '01.01.2022',
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
async def test_cgi_manager_list(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/cgi/index?group_id=3&per-page=100',
                   'POST', CGI_RESPONSE, match_querystring=True)
    aresponses.add('demo.s20.online', '/v2api/1/cgi/index?customer_id=5&per-page=100',
                   'POST', CGI_RESPONSE, match_querystring=True)
    cgi_manager = CGI(
        api_client=api_client,
        entity_class=entities.CGI,
    )
    with pytest.raises(ValueError):
        await cgi_manager.list()

    cgies = await cgi_manager.list(customer_id=5)

    assert len(cgies) == 1
    cgi = cgies[0]
    assert cgi.id == 1
    assert cgi.customer_id == 5
    assert cgi.group_id == 3
    assert cgi.b_date == datetime.date(2021, 1, 1)
    assert cgi.e_date == datetime.date(2022, 1, 1)

    cgies = await cgi_manager.list(group_id=3)
    assert len(cgies) == 1
    assert cgi.id == 1
    assert cgi.customer_id == 5
    assert cgi.group_id == 3
    assert cgi.b_date == datetime.date(2021, 1, 1)
    assert cgi.e_date == datetime.date(2022, 1, 1)


@pytest.mark.asyncio
async def test_cgi_manager_get(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/cgi/index?group_id=3&per-page=100',
                   'POST', CGI_RESPONSE, match_querystring=True)
    aresponses.add('demo.s20.online', '/v2api/1/cgi/index?customer_id=5&per-page=100',
                   'POST', CGI_RESPONSE, match_querystring=True)
    cgi_manager = CGI(
        api_client=api_client,
        entity_class=entities.CGI,
    )
    with pytest.raises(ValueError):
        await cgi_manager.get(id_=1)

    cgi = await cgi_manager.get(id_=1, customer_id=5)

    assert cgi.id == 1
    assert cgi.customer_id == 5
    assert cgi.group_id == 3
    assert cgi.b_date == datetime.date(2021, 1, 1)
    assert cgi.e_date == datetime.date(2022, 1, 1)

    cgi = await cgi_manager.get(id_=1, group_id=3)
    assert cgi.id == 1
    assert cgi.customer_id == 5
    assert cgi.group_id == 3
    assert cgi.b_date == datetime.date(2021, 1, 1)
    assert cgi.e_date == datetime.date(2022, 1, 1)
