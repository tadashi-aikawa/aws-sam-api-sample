import json
from typing import List, Union
from functools import wraps


def omit_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


class InvalidParam():
    def __init__(self, name: str, reason: str):
        self.name = name
        self.reason = reason


class ServerError(Exception):
    def __init__(self, type: str, title: str, status: int, detail: str, instance: str):
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.instance = instance

    def to_json(self):
        return json.dumps(omit_none(self.__dict__), ensure_ascii=False)


class ClientError(Exception):
    def __init__(self, type: str, title: str, status: int, detail: str, invalid_params: List[InvalidParam]=None):
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


