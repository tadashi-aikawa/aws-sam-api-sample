from aws_sam_sample.dao import find_member, Member, Base
from aws_sam_sample.session import Session, engine


class TestFindMember():

    def test_found(self):
        Base.metadata.create_all(bind=engine)
        session = Session()
        session.add_all([
            Member(id='0001', name='イチロー', age=40),
            Member(id='0002', name='ジロー', age=30)
        ])
        session.commit()

        actual: Member = find_member('0001')
        assert actual.name == 'イチロー'
        assert actual.age == 40

        session.query(Member).delete()

    def test_not_found(self):
        Base.metadata.create_all(bind=engine)
        session = Session()
        session.add_all([
            Member(id='0001', name='イチロー', age=40),
            Member(id='0002', name='ジロー', age=30)
        ])
        session.commit()

        actual: Member = find_member('9999')
        assert actual is None

        session.query(Member).delete()
