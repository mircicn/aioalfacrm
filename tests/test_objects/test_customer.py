import datetime

import aiohttp
import pytest

from aioalfacrm import crud_objects
from aioalfacrm import models
from aioalfacrm.core import AuthManager, ApiClient
from . import add_auth_request

CUSTOMER_RESPONSE = {
    'page': 0,
    'total': 1,
    'count': 1,
    'items': [
        {
            'id': 1,
            'branch_ids': [1],
            'teacher_ids': [],
            'name': 'User Name',
            'is_study': 1,
            'study_status_id': 3,
            'lead_status_id': 3,
            'lead_source_id': 15,
            'assigned_id': 15,
            'legal_type': 1,
            'legal_name': 'Legal Name',
            'company_id': None,
            'dob': '03.12.2012',
            'balance': '575.00',
            'balance_base': '0.00',
            'balance_bonus': 0,
            'next_lesson_date': None,
            'paid_till': None,
            'last_attend_date': '2020-12-09',
            'b_date': '2020-08-25 17:40:51',
            'e_date': '2030-12-31',
            'note': 'Note',
            'paid_lesson_count': 0,
            'paid_lesson_date': None,
            'phone': [
                '+7(999)999-99-99'
            ],
            'email': [
                'mail@mail.com'
            ],
            'web': [],
            'addr': [],
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
async def test_customer(api_client, aresponses):
    add_auth_request(aresponses)
    aresponses.add('demo.s20.online', '/v2api/1/customer/index', 'POST', CUSTOMER_RESPONSE)

    customer_object = crud_objects.Customer(
        api_client=api_client,
        model_class=models.Customer,
    )
    customers = await customer_object.list()
    assert len(customers) == 1

    customer = customers[0]

    assert customer.id == 1
    assert customer.branch_ids == [1]
    assert customer.teacher_ids == []
    assert customer.name == 'User Name'
    assert customer.is_study is True
    assert customer.study_status_id == 3
    assert customer.lead_status_id == 3
    assert customer.lead_source_id == 15
    assert customer.assigned_id == 15
    assert customer.legal_type == 1
    assert customer.legal_name == 'Legal Name'
    assert customer.company_id is None
    assert customer.dob == datetime.date(2012, 12, 3)
    assert customer.balance == 575.0
    assert customer.balance_base == 0
    assert customer.paid_lesson_count == 0
    assert customer.last_attend_date == datetime.date(2020, 12, 9)
    assert customer.b_date == datetime.datetime(2020, 8, 25, 17, 40, 51)
    assert customer.e_date == datetime.date(2030, 12, 31)
    assert customer.note == 'Note'
    assert customer.phone == ['+7(999)999-99-99']
    assert customer.email == ['mail@mail.com']
    assert customer.web == []
    assert customer.addr == []
