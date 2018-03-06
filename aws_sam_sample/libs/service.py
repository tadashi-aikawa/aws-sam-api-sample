from typing import Optional

from aws_sam_sample.libs.dao import find_member, Member


def fetch_member(id: str) -> Optional[Member]:
    return find_member(id)

