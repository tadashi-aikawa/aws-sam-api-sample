from aws_sam_sample.service import fetch_member
from aws_sam_sample.dao import Member


class TestFetchMember():

    def test_found(self, monkeypatch):
        monkeypatch.setattr(
            'aws_sam_sample.service.find_member',
            lambda id: Member(id='9999', name='クロー', age=19)
        )

        actual: Member = fetch_member('dummy')
        assert actual.id == '9999'
        assert actual.name == 'クロー'
        assert actual.age == 19

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(
            'aws_sam_sample.service.find_member',
            lambda id: None
        )

        actual: Member = fetch_member('any')
        assert actual is None

