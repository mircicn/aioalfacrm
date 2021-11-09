import datetime

from aioalfacrm.models import Customer


def test_init_customer():
    customer = Customer(
        id_=1,
        name='Name',
        branch_ids=[1, 2, 3],
        teacher_ids=[1],
        is_study=False,
        study_status_id=1,
        lead_status_id=2,
        assigned_id=3,
        legal_type=2,
        legal_name='legal name',
        company_id=2,
        dob=datetime.date(2021, 1, 1),
        balance=10.2,
        balance_base=10.2,
        last_attend_date=datetime.date(2022, 2, 2),
        b_date=datetime.datetime(2023, 3, 3, 13, 0, 0),
        e_date=datetime.date(2024, 4, 4),
        paid_lesson_count=2,
        phone=['+79999999999'],
        email=['test@mail.test'],
        web=[],
        addr=[],
        note='note',
    )

    assert customer.id == 1
    assert customer.name == 'Name'
    assert customer.branch_ids == [1, 2, 3]
    assert customer.teacher_ids == [1]
    assert customer.is_study is False
    assert customer.study_status_id == 1
    assert customer.lead_status_id == 2
    assert customer.assigned_id == 3
    assert customer.legal_type == 2
    assert customer.legal_name == 'legal name'
    assert customer.company_id == 2
    assert customer.dob == datetime.date(2021, 1, 1)
    assert customer.balance == 10.2
    assert customer.balance_base == 10.2
    assert customer.last_attend_date == datetime.date(2022, 2, 2)
    assert customer.b_date == datetime.datetime(2023, 3, 3, 13, 0, 0)
    assert customer.e_date == datetime.date(2024, 4, 4)
    assert customer.paid_lesson_count == 2
    assert customer.phone == ['+79999999999']
    assert customer.email == ['test@mail.test']
    assert customer.web == []
    assert customer.addr == []
    assert customer.note == 'note'
