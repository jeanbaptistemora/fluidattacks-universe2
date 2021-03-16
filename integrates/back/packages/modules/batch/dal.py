# Standard libraries
import logging
import logging.config
from typing import (
    List,
    Optional,
)

# Third party libraries
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local imports
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import DynamoDelete
from batch.types import BatchProcessing
from newutils.encodings import safe_encode

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'fi_async_processing'


def mapping_to_key(items: List[str]) -> str:
    return '.'.join([
        safe_encode(attribute_value)
        for attribute_value in sorted(items)
    ])


async def delete_action(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
    time: str,
) -> bool:
    try:
        return await dynamodb.async_delete_item(
            delete_attrs=DynamoDelete(Key=dict(
                pk=mapping_to_key([
                    action_name, additional_info, entity, subject, time
                ]),
            )),
            table=TABLE_NAME,
        )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return False


async def is_action_by_key(*, key: str) -> bool:
    query_attrs = dict(
        KeyConditionExpression=Key('pk').eq(key)
    )
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)

    if not response_items:
        return False

    return bool(response_items[0])


async def get_action(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
    time: str,
) -> Optional[BatchProcessing]:
    key: str = mapping_to_key([
        action_name, additional_info, entity, subject, time
    ])
    query_attrs = dict(
        KeyConditionExpression=Key('pk').eq(key)
    )
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)

    if not response_items:
        return None

    item = response_items[0]
    return BatchProcessing(
        key=item['pk'],
        action_name=item['action_name'].lower(),
        entity=item['entity'].lower(),
        subject=item['subject'].lower(),
        time=item['time'],
        additional_info=item.get('additional_info', ''),
    )


async def get_actions() -> List[BatchProcessing]:
    items = await dynamodb.async_scan(
        table=TABLE_NAME,
        scan_attrs=dict()
    )

    return [
        BatchProcessing(
            key=item['pk'],
            action_name=item['action_name'].lower(),
            entity=item['entity'].lower(),
            subject=item['subject'].lower(),
            time=item['time'],
            additional_info=item.get('additional_info', ''),
        )
        for item in items
    ]


async def put_action_to_dynamodb(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
) -> bool:
    try:
        return await dynamodb.async_put_item(
            item=dict(
                pk=mapping_to_key([
                    action_name, additional_info, entity, subject, time
                ]),
                action_name=action_name,
                additional_info=additional_info,
                entity=entity,
                subject=subject,
            ),
            table=TABLE_NAME,
        )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return False
