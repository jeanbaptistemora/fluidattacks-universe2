import logging
import logging.config
from typing import (
    cast,
    List,
)

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from back.settings import LOGGING
from backend.typing import Event as EventType
from dynamodb import operations_legacy as dynamodb_ops
from s3 import operations as s3_ops
from __init__ import (
    FI_AWS_S3_BUCKET,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'fi_events'


async def create(
        event_id: str,
        group_name: str,
        event_attributes: EventType) -> bool:
    success = False
    try:
        event_attributes.update({
            'event_id': event_id,
            'project_name': group_name
        })
        success = await dynamodb_ops.put_item(TABLE_NAME, event_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def get_event(event_id: str) -> EventType:
    """ Retrieve all attributes from an event """
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('event_id').eq(event_id),
        'Limit': 1
    }
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]
    return response


async def list_group_events(group_name: str) -> List[str]:
    key_exp = Key('project_name').eq(group_name)
    query_attrs = {
        'KeyConditionExpression': key_exp,
        'IndexName': 'project_events',
        'ProjectionExpression': 'event_id'
    }
    events = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    return [event['event_id'] for event in events]


async def save_evidence(file_object: object, file_name: str) -> bool:
    return cast(
        bool,
        await s3_ops.upload_memory_file(
            FI_AWS_S3_BUCKET,
            file_object,
            file_name
        )
    )


async def search_evidence(file_name: str) -> List[str]:
    return cast(
        List[str],
        await s3_ops.list_files(FI_AWS_S3_BUCKET, file_name)
    )


async def sign_url(file_url: str) -> str:
    return cast(
        str,
        await s3_ops.sign_url(file_url, 10, FI_AWS_S3_BUCKET)
    )


async def remove_evidence(file_name: str) -> bool:
    return cast(
        bool,
        await s3_ops.remove_file(FI_AWS_S3_BUCKET, file_name)
    )


async def update(event_id: str, data: EventType) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {'event_id': event_id},
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
