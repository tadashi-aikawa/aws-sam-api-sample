from typing import Optional, NamedTuple

from aws_sam_sample.service import fetch_member
from aws_sam_sample.dao import find_member, Member
from aws_sam_sample.libs.saucisse import endpoint, ClientError

class Form(NamedTuple):
    id: str

    @classmethod
    def from_event(cls, event) -> 'Form':
        id: str = event['pathParameters'].get('id')
        if len(id) != 4:
            raise ClientError(
                type='/member', title='Paramater error', detail='...', status=400,
                invalid_params=[{'name': 'id', 'reason': 'Length must be 4'}]
            )
        return cls(id=id)


@endpoint(form=Form)
def member(form: Form):
    member: Optional[Member] = fetch_member(form.id)
    if not member:
        raise ClientError(type='/member', title='Member is not found', detail=f"id: {form.id}", status=404)

    return {
        'id': member.id,
        'name': member.name,
    }

