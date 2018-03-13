import json
from functools import wraps
from typing import Dict, List, Optional, Type, Union

from marshmallow import Schema


def omit_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


class HttpError(Exception):
    title: str
    status: int
    type: Optional[str]
    detail: Optional[str]

    def __init__(self, title, status, type_=None, detail=None):
        self.title = title
        self.status = status
        self.type = type_
        self.detail = detail

    def to_json(self):
        return json.dumps(omit_none(self.__dict__), ensure_ascii=False)


class ClientError(HttpError):
    pass


class BadRequestError(ClientError):
    invalid_params: Dict[str, List[str]]

    def __init__(self, type, invalid_params):
        super().__init__(
            title="Your request parameters didn't validate.",
            status=400,
            type_=type)
        self.invalid_params = invalid_params


class NotFoundError(ClientError):
    def __init__(self, title, detail):
        super().__init__(title=title, status=404, detail=detail)


class ServerError(HttpError):
    pass


class Form:
    _type: Optional[str]

    class FormSchema(Schema):
        pass

    @classmethod
    def from_dict(cls, d: dict) -> 'Form':
        errors = cls.FormSchema().validate(d)
        if errors:
            raise BadRequestError(type=cls._type, invalid_params=errors)

        ins = cls()
        properties = cls.__annotations__.items()
        for n, t in properties:
            setattr(ins, n, d.get(n))
        return ins


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
