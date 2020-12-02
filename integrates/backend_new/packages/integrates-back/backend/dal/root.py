# Standard
import logging
import uuid
from typing import Any, Dict, Optional, Tuple

# Third party
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local
from backend.dal.helpers import dynamodb
from backend.exceptions import UnavailabilityError
from fluidintegrates.settings import LOGGING


# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)
TABLE_NAME: str = 'fi_roots'


async def get_root_by_id(root_id: str) -> Optional[Dict[str, Any]]:
    results = await dynamodb.async_query(
        TABLE_NAME,
        {
            'IndexName': 'roots_index',
            'KeyConditionExpression': Key('sk').eq(root_id)
        }
    )
    return results[0] if results else None


async def get_roots_by_group(group_name: str) -> Tuple[Dict[str, Any], ...]:
    return tuple(await dynamodb.async_query(
        TABLE_NAME,
        {
            'KeyConditionExpression': (
                Key('pk').eq(f'GROUP#{group_name}') &
                Key('sk').begins_with('ROOT#')
            ),
        }
    ))


async def create(group_name: str, root_attributes: Dict[str, Any]) -> None:
    try:
        await dynamodb.async_put_item(
            TABLE_NAME,
            {
                'pk': f'GROUP#{group_name}',
                'sk': f'ROOT#{uuid.uuid4()}',
                **root_attributes
            }
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex


async def update(
    group_name: str,
    root_id: str,
    root_attributes: Dict[str, Any]
) -> None:
    try:
        set_actions: Tuple[str, ...] = tuple(
            f'#{attribute} = :{attribute}'
            for attribute in root_attributes
        )
        attribute_names: Dict[str, str] = {
            f'#{attribute}': attribute
            for attribute in root_attributes
        }
        attribute_values: Dict[str, Any] = {
            f':{attribute}': root_attributes[attribute]
            for attribute in root_attributes
        }

        await dynamodb.async_update_item(
            TABLE_NAME,
            {
                'ExpressionAttributeNames': attribute_names,
                'ExpressionAttributeValues': attribute_values,
                'Key': {
                    'pk': f'GROUP#{group_name}',
                    'sk': root_id
                },
                'UpdateExpression': f'SET {",".join(set_actions)}',
            }
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex
