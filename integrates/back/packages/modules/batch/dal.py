# Standard libraries
import logging
import logging.config
from typing import (
    List,
    Optional,
)

# Third party libraries
import aioboto3
from aioextensions import collect
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local imports
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import DynamoDelete
from batch.types import BatchProcessing
from newutils.context import (
    AWS_DYNAMODB_ACCESS_KEY,
    AWS_DYNAMODB_SECRET_KEY,
    AWS_SESSION_TOKEN,
    CI_COMMIT_REF_NAME,
    ENVIRONMENT
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
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
                time=time,
            ),
            table=TABLE_NAME,
        )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return False


async def put_action_to_batch(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
) -> bool:
    env: str = 'DEV' if ENVIRONMENT == 'development' else 'PROD'
    try:
        resource_options = dict(
            service_name='batch',
            aws_access_key_id=AWS_DYNAMODB_ACCESS_KEY,
            aws_secret_access_key=AWS_DYNAMODB_SECRET_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
        )
        async with aioboto3.client(**resource_options) as batch:
            await batch.submit_job(
                jobName='integrates-asynchronous-processing',
                jobQueue='spot_now',
                jobDefinition='default',
                containerOverrides={
                    'vcpus': 2,
                    'command': [
                        './m',
                        'integrates.batch',
                        env.lower(),
                        action_name,
                        subject,
                        entity,
                        time,
                        additional_info,
                    ],
                    'environment': [
                        *(
                            [{
                                'name': 'AWS_SESSION_TOKEN',
                                'value': AWS_SESSION_TOKEN
                            }]
                            if AWS_SESSION_TOKEN else []
                        ),
                        {
                            'name': 'CI',
                            'value': 'true'
                        },
                        {
                            'name': 'CI_COMMIT_REF_NAME',
                            'value': CI_COMMIT_REF_NAME
                        },
                        {
                            'name': f'INTEGRATES_{env}_AWS_ACCESS_KEY_ID',
                            'value': AWS_DYNAMODB_ACCESS_KEY
                        },
                        {
                            'name': f'INTEGRATES_{env}_AWS_SECRET_ACCESS_KEY',
                            'value': AWS_DYNAMODB_SECRET_KEY
                        },
                    ],
                    'memory': 7200,
                },
                retryStrategy={
                    'attempts': 1,
                },
                timeout={
                    'attemptDurationSeconds': 3600
                },
            )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return False
    else:
        return True


async def put_action(
    *,
    action_name: str,
    entity: str,
    subject: str,
    additional_info: str,
) -> bool:
    time: str = str(get_as_epoch(get_now()))
    action = dict(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
    )

    return all(
        await collect((
            put_action_to_batch(**action),
            put_action_to_dynamodb(**action)
        ))
    )
