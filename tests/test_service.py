from aws_sam_sample.service import fetch_member, fetch_account
from aws_sam_sample.dao import Member
from aws_sam_sample.storage import Account


class TestFetchAccount():

    def test_found(self, monkeypatch):
        monkeypatch.setattr(
            'aws_sam_sample.storage.fetch_account',
            lambda name: Account(name='taro', last_login='2000-01-01T09:00:00+09:00')
        )

        actual: Account = fetch_account('any')
        assert actual.name == 'taro'
        assert actual.last_login == '2000-01-01T09:00:00+09:00'

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(
            'aws_sam_sample.storage.fetch_account',
            lambda name: None
        )

        actual: Account = fetch_account('any')
        assert actual is None


class TestFetchMember():

    def test_found(self, monkeypatch):
        monkeypatch.setattr(
            'aws_sam_sample.service.find_member',
            lambda id: Member(id='9999', name='クロー', age=19)
        )

        actual: Member = fetch_member('any')
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
