from aws_sam_sample.libs.dao import find_member, Member, Base
from aws_sam_sample.libs.session import Session, engine


def test_hoge():
    Base.metadata.create_all(bind=engine)
    session = Session()
    session.add_all([
        Member(id=1, name='イチロー', age=40),
        Member(id=2, name='ジロー', age=30)
    ])
    session.commit()

    actual: Member = find_member(1)
    assert actual.name == 'イチロー'
    assert actual.age == 40

