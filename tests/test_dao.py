from aws_sam_sample.libs.dao import find_human, Human, Base
from aws_sam_sample.libs.session import Session, engine


def test_hoge():
    Base.metadata.create_all(bind=engine)
    session = Session()
    session.add_all([
        Human(id=1, name='tadashi-aikawa'),
        Human(id=2, name='Ichiro')
    ])
    session.commit()

    actual: Human = find_human(1)
    assert actual.name == 'tadashi-aikawa'

