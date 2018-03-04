from aws_sam_sample.libs.dao import find_member, Member
from aws_sam_sample.libs.models import Event


def main(event, context):
    e: Event = Event(**event)
    member: Member = find_member(e.id)
    return {
        'id': member.id,
        'name': member.name
    }

