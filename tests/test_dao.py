import pytest

from aws_sam_sample.dao import Base, Member, find_member
from aws_sam_sample.session import Session, engine


@pytest.fixture(autouse=True)
def initdb():
    Base.metadata.create_all(bind=engine)
    session = Session()
    session.add_all([
        Member(id='0001', name='イチロー', age=40),
        Member(id='0002', name='ジロー', age=30)
    ])
    session.commit()

    yield

    session.query(Member).delete()


class TestFindMember():
    def test_found(self):
        actual: Member = find_member('0001')
        assert actual.name == 'イチロー'
        assert actual.age == 40

    def test_not_found(self):
        actual: Member = find_member('9999')
        assert actual is None
