from typing import Optional

import aiohttp
import pytest

from aioalfacrm import fields
from aioalfacrm.core import AuthManager, ApiClient
from aioalfacrm.core.exceptions import NotFound
from aioalfacrm.core.model import AlfaObject
from aioalfacrm.core.object_ import BaseCRUDAlfaObject, AlfaCRUDObject


class TestClass(BaseCRUDAlfaObject):
    object_name = 'customer'


class TestCRUDAlfaObject(AlfaCRUDObject):
    object_name = 'customer'


class TestModel(AlfaObject):
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


@pytest.mark.asyncio
async def test_base_alfa_crud_object_list(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 10, 'count': 1, 'page': 1, 'items': [{'field1': 1}]},
        body_pattern='{"page": 1}'
    )
    a = TestClass(
        api_client=api_client,
    )

    data = await a._list(page=1, count=1)
    assert data == {'total': 10, 'count': 1, 'page': 1, 'items': [{'field1': 1}]}


@pytest.mark.asyncio
async def test_base_alfa_crud_object_get(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 1, 'count': 1, 'page': 0, 'items': [{'field1': 1}]},
        body_pattern='{"id": 2}'
    )

    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 0, 'count': 0, 'page': 0, 'items': []},
        body_pattern='{"id": 3}'
    )

    a = TestClass(
        api_client=api_client
    )

    data = await a._get(id_=2)
    assert data == {'field1': 1}

    with pytest.raises(NotFound):
        await a._get(id_=3)


@pytest.mark.asyncio
async def test_base_alfa_crud_object_update(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/update', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 2, 'field1': 2}},
        body_pattern='{"field1": 2}'
    )

    a = TestClass(
        api_client=api_client
    )

    data = await a._update(id_=2, field1=2)
    assert data == {'id': 2, 'field1': 2}


@pytest.mark.asyncio
async def test_base_alfa_crud_object_create(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/create', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 3, 'field1': 10}},
        body_pattern='{"field1": 10}'
    )

    a = TestClass(
        api_client=api_client,
    )
    data = await a._create(field1=10)
    assert data == {'id': 3, 'field1': 10}


@pytest.mark.asyncio
async def test_base_alfa_crud_object_save(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/create', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 4, 'field1': 11}},
        body_pattern='{"field1": 11}'
    )
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/update', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 4, 'field1': 12}},
        body_pattern='{"field1": 12}'
    )

    a = TestClass(
        api_client=api_client,
    )

    new_customer = await a._save(field1=11)
    assert new_customer == {'id': 4, 'field1': 11}
    new_customer['field1'] = 12
    updated_customer = await a._save(**new_customer)
    assert updated_customer == {'id': 4, 'field1': 12}


@pytest.mark.asyncio
async def test_alfa_crud_object_list(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 10, 'count': 1, 'page': 1, 'items': [{'id': 1, 'field1': 1}]},
        body_pattern='{"page": 1}'
    )

    a = TestCRUDAlfaObject(
        api_client=api_client,
        model_class=TestModel,
    )

    customers = await a.list(page=1, count=1)
    assert len(customers) == 1
    customer = customers[0]
    assert customer.serialize() == {'id': 1, 'field1': 1}


@pytest.mark.asyncio
async def test_alfa_crud_object_get(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 1, 'count': 1, 'page': 0, 'items': [{'id': 2, 'field1': 1}]},
        body_pattern='{"id": 2}'
    )

    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 0, 'count': 0, 'page': 0, 'items': []},
        body_pattern='{"id": 3}'
    )

    a = TestCRUDAlfaObject(
        api_client=api_client,
        model_class=TestModel,
    )

    customer = await a.get(2)
    assert customer.serialize() == {'id': 2, 'field1': 1}
    with pytest.raises(NotFound):
        await a.get(3)


@pytest.mark.asyncio
async def test_alfa_crud_object_save(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/create', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 4, 'field1': 11}},
        body_pattern='{"field1": 11}'
    )
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/update', 'POST',
        {'success': True, 'errors': [], 'model': {'id': 4, 'field1': 12}},
        body_pattern='{"field1": 12}'
    )
    a = TestCRUDAlfaObject(
        api_client=api_client,
        model_class=TestModel,
    )

    new_customer = TestModel(
        field1=11,
    )

    created_customer = await a.save(new_customer)
    assert created_customer.serialize() == {'id': 4, 'field1': 11}
    created_customer.field1 = 12
    updated_customer = await a.save(created_customer)
    assert updated_customer.serialize() == {'id': 4, 'field1': 12}


@pytest.mark.asyncio
async def test_alfa_crut_object_page(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add(
        'demo.s20.online', '/v2api/1/customer/index', 'POST',
        {'total': 10, 'count': 2, 'page': 1, 'items': [{'id': 1, 'field1': 1}, {'id': 2, 'field1': 2}]},
        body_pattern='{"page": 1}'
    )
    a = TestCRUDAlfaObject(
        api_client=api_client,
        model_class=TestModel,
    )
    page = await a.page(page=1, count=2)

    assert page.items == [TestModel(id_=1, field1=1), TestModel(id_=2, field1=2)]
    assert page.number == 1
    assert page.total == 10


@pytest.mark.asyncio
async def test_alfa_crud_object_paginator(api_client):
    a = TestCRUDAlfaObject(
        api_client=api_client,
        model_class=TestModel
    )

    paginator = a.paginator(start_page=0, page_size=1)

    assert paginator._object == a
