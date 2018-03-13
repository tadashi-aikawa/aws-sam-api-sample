import json
from functools import wraps
from typing import Dict, List, Optional, Type, Union

from marshmallow import Schema


def omit_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


class Form:
    class FormSchema(Schema):
        pass

    @classmethod
    def from_dict(cls, d: dict) -> 'Form':
        errors = cls.FormSchema().validate(d)
        if errors:
            raise ClientError(
                type='https://github.com/tadashi-aikawa/aws-sam-sample',
                title="Your request parameters didn't validate.",
                invalid_params=errors,
                status=400)

        ins = cls()
        properties = cls.__annotations__.items()
        for n, t in properties:
            setattr(ins, n, d.get(n))
        return ins


class ServerError(Exception):
    def __init__(self, type: str, title: str, status: int, detail: str,
                 instance: str) -> None:
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.instance = instance

    def to_json(self):
        return json.dumps(omit_none(self.__dict__), ensure_ascii=False)


class ClientError(Exception):
    def __init__(self,
                 type: str,
                 title: str,
                 status: int,
                 detail: Optional[str] = None,
                 invalid_params: Dict[str, List[str]] = None) -> None:
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.invalid_params = invalid_params

    def to_json(self):
        return json.dumps(omit_none(self.__dict__), ensure_ascii=False)


def create_error(error: Union[ClientError, ServerError]):
    return {
        'statusCode': error.status,
        'headers': {
            'Content-Type': 'application/problem+json; charset=utf8'
        },
        'body': error.to_json()
    }


def create_response(body: dict):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf8'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }


def endpoint(form: Type[Form]):
    def endpoint_wrapper(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                d: dict = event['pathParameters']
                d.update(event['queryStringParameters'])
                return create_response(func(form.from_dict(d)))
            except ClientError as err:
                return create_error(err)
            except ServerError as err:
                return create_error(err)

        return wrapper

    return endpoint_wrapper
