import json
from functools import wraps
from typing import List, Union

from marshmallow import Schema, ValidationError


def omit_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


class Form(Schema):
    pass


class InvalidParam():
    def __init__(self, name: str, reason: str) -> None:
        self.name = name
        self.reason = reason


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
                 detail: str,
                 invalid_params: List[InvalidParam] = None) -> None:
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


def endpoint(form: Form):
    def endpoint_wrapper(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                d: dict = event['pathParameters']
                d.extend(event['queryParameters'])
                return create_response(func(form.load(d)))
            except ValidationError as err:
                print('ValidationError')
                print(err)
                return create_error(err)
            except ClientError as err:
                return create_error(err)
            except ServerError as err:
                return create_error(err)

        return wrapper

    return endpoint_wrapper
