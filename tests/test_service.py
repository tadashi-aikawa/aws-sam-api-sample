import pytest

from aws_sam_sample.dao import Member
from aws_sam_sample.service import fetch_account, fetch_member
from aws_sam_sample.storage import Account


@pytest.fixture()
def fetch_account_returns(monkeypatch):
    def stub(account: Account):
        monkeypatch.setattr('aws_sam_sample.storage.fetch_account',
                            lambda name: account)

    yield stub


@pytest.fixture()
def find_member_returns(monkeypatch):
    def stub(member: Member):
        monkeypatch.setattr('aws_sam_sample.service.find_member',
                            lambda id: member)

    yield stub


class TestFetchAccount:
    def test_found(self, fetch_account_returns):
        fetch_account_returns(
            Account(name='taro', last_login='2000-01-01T09:00:00+09:00'))

        actual: Account = fetch_account('any')
        assert actual.name == 'taro'
        assert actual.last_login == '2000-01-01T09:00:00+09:00'

    def test_not_found(self, fetch_account_returns):
        fetch_account_returns(None)

        actual: Account = fetch_account('any')
        assert actual is None


class TestFetchMember():
    def test_found(self, find_member_returns):
        find_member_returns(Member(id='9999', name='クロー', age=19))

        actual: Member = fetch_member('any')
        assert actual.id == '9999'
        assert actual.name == 'クロー'
        assert actual.age == 19

    def test_not_found(self):
        find_member_returns(None)

        actual: Member = fetch_member('any')
        assert actual is None
