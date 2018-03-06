import json
from typing import Optional, NamedTuple, List, Union
from functools import wraps

from aws_sam_sample.libs.service import fetch_member
from aws_sam_sample.libs.dao import find_member, Member
from aws_sam_sample.libs.models import Event


#------- ライブラリに切り出してもいい --------#

class ServerError(Exception):
    def __init__(self, type: str, title: str, status: int, detail: str, instance: str):
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.instance = instance

    def to_json(self):
        return json.dumps({k: v for (k, v) in self.__dict__.items() if v is not None}, ensure_ascii=False)


class InvalidParam():
    def __init__(self, name: str, reason: str):
        self.name = name
        self.reason = reason


class ClientError(Exception):
    def __init__(self, type: str, title: str, status: int, detail: str, invalid_params: List[InvalidParam]=None):
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.invalid_params = invalid_params

    def to_json(self):
        return json.dumps({k: v for (k, v) in self.__dict__.items() if v is not None}, ensure_ascii=False)


def create_error(error: Union[ClientError, ServerError]):
    return {
        'statusCode': error.status,
        'headers': { 'Content-Type': 'application/problem+json; charset=utf8' },
        'body': error.to_json()
    }


def create_response(body: dict):
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json; charset=utf8' },
        'body': json.dumps(body, ensure_ascii=False)
    }

def endpoint(form):
    def endpoint_wrapper(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                return create_response(func(form.from_event(event)))
            except ClientError as err:
                return create_error(err)
            except ServerError as err:
                return create_error(err)
        return wrapper
    return endpoint_wrapper


#------- Formとして切り出してもよい マシュマロ使えればGood --------#

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


#------- 純粋なcontrollerはここだけ --------#

@endpoint(form=Form)
def member(form: Form):
    member: Optional[Member] = fetch_member(form.id)
    if not member:
        raise ClientError(type='/member', title='Member is not found', detail=f"id: {form.id}", status=404)

    return {
        'id': member.id,
        'name': member.name,
    }

