from aioalfacrm.models import Subject


def test_inif_subject():
    subject = Subject(
        id_=1,
        name='name'
    )

    assert subject.id == 1
    assert subject.name == 'name'
