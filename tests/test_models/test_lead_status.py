from aioalfacrm.models import LeadStatus


def test_init_lead_status():
    lead_status = LeadStatus(
        id_=1,
        name='name',
        is_enabled=True,
    )

    assert lead_status.id == 1
    assert lead_status.name == 'name'
    assert lead_status.is_enabled is True
