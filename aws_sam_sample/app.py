from aws_sam_sample.libs.dao import find_human, Human
from aws_sam_sample.libs.models import Event


def main(event, context):
    e: Event = Event(**event)

    human: Human = find_human(e.id)
    return {
        'id': human.id,
        'name': human.name
    }
