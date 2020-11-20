"""DAL functions for events."""
import logging
from typing import List

from aioextensions import in_thread
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.dal.helpers import cloudfront, dynamodb, s3
from backend.typing import Event as EventType
from fluidintegrates.settings import LOGGING

from __init__ import (
    FI_AWS_S3_BUCKET,
    FI_CLOUDFRONT_RESOURCES_DOMAIN
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'fi_events'


async def create(
        event_id: str,
        project_name: str,
        event_attributes: EventType) -> bool:
    success = False
    try:
        event_attributes.update({
            'event_id': event_id,
            'project_name': project_name
        })
        success = await dynamodb.async_put_item(TABLE_NAME, event_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


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
        'Key': {
            'event_id': event_id
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
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
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]

    return response


async def save_evidence(file_object: object, file_name: str) -> bool:
    return await s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_BUCKET,
        file_object,
        file_name
    )


async def remove_evidence(file_name: str) -> bool:
    return await s3.remove_file(FI_AWS_S3_BUCKET, file_name)  # type: ignore


async def sign_url(file_url: str) -> str:
    return await in_thread(
        cloudfront.sign_url,
        FI_CLOUDFRONT_RESOURCES_DOMAIN,
        file_url,
        1.0 / 6
    )


async def search_evidence(file_name: str) -> List[str]:
    return await s3.list_files(FI_AWS_S3_BUCKET, file_name)  # type: ignore
