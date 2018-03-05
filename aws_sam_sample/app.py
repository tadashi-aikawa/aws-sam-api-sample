from aws_sam_sample.libs.dao import find_member, Member
from aws_sam_sample.libs.models import Event
import json


def main(event, context):
    id = event['pathParameters']['id']
    # e: Event = Event(**event)
    # member: Member = find_member(e.id)
    member: Member = find_member(id)
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json; charset=utf8' },
        'body': json.dumps({
            'id': member.id,
            'name': member.name
        }, ensure_ascii=False)
    }

