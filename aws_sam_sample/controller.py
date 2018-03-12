from typing import NamedTuple, Optional

from aws_sam_sample.dao import Member
from aws_sam_sample.libs.saucisse import ClientError, InvalidParam, endpoint
from aws_sam_sample.service import fetch_member
from aws_sam_sample.storage import Account, fetch_account


class AccountForm(NamedTuple):
    name: str

    @classmethod
    def from_event(cls, event) -> 'AccountForm':
        name: str = event['pathParameters'].get('name')
        return cls(name=name)


class MemberForm(NamedTuple):
    id: str

    @classmethod
    def from_event(cls, event) -> 'MemberForm':
        id: str = event['pathParameters'].get('id')
        if len(id) != 4:
            raise ClientError(
                type='/member',
                title='Paramater error',
                detail='...',
                status=400,
                invalid_params=[
                    InvalidParam(name='id', reason='Length must be 4')
                ])
        return cls(id=id)


@endpoint(form=AccountForm)
def account(form: AccountForm):
    account: Optional[Account] = fetch_account(form.name)
    if not account:
        raise ClientError(
            type='/account',
            title='Account is not found',
            detail=f"name: {form.name}",
            status=404)

    return {
        'name': account.name,
        'last_login': account.last_login,
    }


@endpoint(form=MemberForm)
def member(form: MemberForm):
    member: Optional[Member] = fetch_member(form.id)
    if not member:
        raise ClientError(
            type='/member',
            title='Member is not found',
            detail=f"id: {form.id}",
            status=404)

    return {
        'id': member.id,
        'name': member.name,
    }
