from typing import Optional

from aws_sam_sample.dao import Member
from aws_sam_sample.libs.saucisse import Form, NotFoundError, endpoint
from aws_sam_sample.service import fetch_member
from aws_sam_sample.storage import Account, fetch_account
from marshmallow import Schema, fields, validate


class AccountForm(Form):
    name: str
    _type: str = 'https://github.com/tadashi-aikawa/aws-sam-sample'

    class FormSchema(Schema):
        name: str = fields.String()


class MemberForm(Form):
    id: str
    _type: str = 'https://github.com/tadashi-aikawa/aws-sam-sample'

    class FormSchema(Schema):
        id: str = fields.String(validate=validate.Length(equal=4))


@endpoint(form=AccountForm)
def account(form: AccountForm):
    account: Optional[Account] = fetch_account(form.name)
    if not account:
        raise NotFoundError(
            title='Account is not found', detail=f"name: {form.name}")

    return {
        'name': account.name,
        'last_login': account.last_login,
    }


@endpoint(form=MemberForm)
def member(form: MemberForm):
    member: Optional[Member] = fetch_member(form.id)
    if not member:
        raise NotFoundError(
            title='Member is not found', detail=f"id: {form.id}")

    return {
        'id': member.id,
        'name': member.name,
    }
