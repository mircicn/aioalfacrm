import datetime

from aioalfacrm.entities import CustomerTariff


def test_init_customer_tariff():
    customer_tariff = CustomerTariff(
        id_=1,
        customer_id=2,
        tariff_id=3,
        subject_ids=[4, 5],
        lesson_type_ids=[6, 7],
        is_separate_balance=False,
        balance=2.1,
        paid_count=2,
        paid_till=datetime.datetime(2021, 1, 1, 14, 2, 1),
        note='Note',
        b_date=datetime.date(2021, 1, 1),
        e_date=datetime.date(2022, 1, 1),
        paid_lesson_count=2,
    )

    assert customer_tariff.id == 1
    assert customer_tariff.customer_id == 2
    assert customer_tariff.tariff_id == 3
    assert customer_tariff.subject_ids == [4, 5]
    assert customer_tariff.lesson_type_ids == [6, 7]
    assert customer_tariff.is_separate_balance is False
    assert customer_tariff.balance == 2.1
    assert customer_tariff.paid_count == 2
    assert customer_tariff.paid_till == datetime.datetime(2021, 1, 1, 14, 2, 1)
    assert customer_tariff.note == 'Note'
    assert customer_tariff.b_date == datetime.date(2021, 1, 1)
    assert customer_tariff.e_date == datetime.date(2022, 1, 1)
    assert customer_tariff.paid_lesson_count == 2
