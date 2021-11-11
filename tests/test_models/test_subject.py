from aioalfacrm.models import Subject


def test_inif_subject():
    subject = Subject(
        id_=1,
        name='name',
        weight=4,
    )

    assert subject.id == 1
    assert subject.name == 'name'
    assert subject.weight == 4
