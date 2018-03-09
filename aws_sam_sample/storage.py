import boto3
import json
from os import environ as env
from typing import NamedTuple


s3 = boto3.resource(
    's3',
) if 'S3_ENDPOINT' not in env else boto3.resource(
    's3',
    aws_access_key_id='accessKey1',
    aws_secret_access_key='verySecretKey1',
    endpoint_url=env.get('S3_ENDPOINT'),
)


class Account(NamedTuple):
    name: str
    # TODO: Use pendulum
    last_login: str


def fetch_account(name: str) -> Account:
    try:
        account = s3.Object(env.get('BUCKET'), f'{name}.json')
        d = json.loads(account.get().get('Body').read().decode('utf8'))
        return Account(name=name, last_login=d['last_login'])
    except s3.meta.client.exceptions.NoSuchKey:
        return None
