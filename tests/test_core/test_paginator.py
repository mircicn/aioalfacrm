from typing import Optional, List

import aiohttp
import pytest

from aioalfacrm import fields
from aioalfacrm.core import AlfaEntity, EntityManager, Paginator, Page, AuthManager, ApiClient


class TestCRUDAlfaObject(EntityManager):
    object_name = 'customer'


class TestModel(AlfaEntity):
    id: Optional[int] = fields.Integer()
    field1: Optional[int] = fields.Integer()

    def __init__(self, id_: Optional[int] = None, field1: Optional[int] = None):
        super(TestModel, self).__init__(field1=field1, id=id_)


def add_auth_request(aresponses):
    aresponses.add('demo.s20.online', '/v2api/auth/login', 'POST', {'token': 'api-token'})


@pytest.fixture
def auth_manager():
    session = aiohttp.ClientSession()
    return AuthManager(
        email='test@test.test',
        api_key='api-key',
        hostname='demo.s20.online',
        session=session,
    )


@pytest.fixture
def api_client(auth_manager: AuthManager):
    return ApiClient(
        hostname='demo.s20.online',
        branch_id=1,
        auth_manager=auth_manager,
        session=auth_manager._session,  # noqa
    )


def test_init_page():
    page = Page(
        number=1,
        items=[1, 2, 3],
        total=10,
    )

    assert page.number == 1
    assert page.items == [1, 2, 3]
    assert page.total == 10


def test_init_paginator(aresponses, api_client):
    crud_object = TestCRUDAlfaObject(
        api_client,
        entity_class=TestModel,
    )

    paginator = Paginator(
        alfa_object=crud_object,
        start_page=0,
        page_size=20,
    )

    assert paginator._object == crud_object
    assert paginator._page_number == 0
    assert paginator._page_size == 20
    assert paginator._page is None
    assert paginator._total == 0


@pytest.mark.asyncio
async def test_paginator(aresponses, api_client):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 3, 'count': 1, 'page': 0, 'items': [{'id': 1, 'field1': 1}]},
        body_pattern='{"page": 0}'
    )
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 3, 'count': 1, 'page': 1, 'items': [{'id': 2, 'field1': 2}]},
        body_pattern='{"page": 1}'
    )
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 3, 'count': 1, 'page': 2, 'items': [{'id': 3, 'field1': 3}]},
        body_pattern='{"page": 2}'
    )

    crud_object = TestCRUDAlfaObject(
        api_client,
        entity_class=TestModel,
    )

    paginator: Paginator[TestModel] = Paginator(
        alfa_object=crud_object,
        start_page=0,
        page_size=1,
    )
    all_pages: List[Page[TestModel]] = []
    async for page in paginator:
        all_pages.append(page)

    assert paginator.total_page == 3

    assert len(all_pages) == 3
    assert all_pages[0].total == 3
    assert all_pages[0].number == 0
    assert all_pages[0].items == [TestModel(id_=1, field1=1)]

    assert all_pages[1].total == 3
    assert all_pages[1].number == 1
    assert all_pages[1].items == [TestModel(id_=2, field1=2)]

    assert all_pages[2].total == 3
    assert all_pages[2].number == 2
    assert all_pages[2].items == [TestModel(id_=3, field1=3)]
