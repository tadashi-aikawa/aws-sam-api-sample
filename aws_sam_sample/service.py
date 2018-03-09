from typing import Optional

from aws_sam_sample.dao import find_member, Member
from aws_sam_sample import storage
from aws_sam_sample.storage import Account


def fetch_account(name: str) -> Optional[Account]:
    return storage.fetch_account(name)


def fetch_member(id: str) -> Optional[Member]:
    return find_member(id)
