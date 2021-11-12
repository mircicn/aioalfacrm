from aioalfacrm.models import LeadReject


def test_init_lead_reject():
    lead_reject = LeadReject(
        id_=1,
        name='Name',
        is_enabled=True,
        weight=0,
    )

    assert lead_reject.id == 1
    assert lead_reject.name == 'Name'
    assert lead_reject.is_enabled is True
    assert lead_reject.weight == 0
