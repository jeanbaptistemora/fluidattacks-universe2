# Standard
import logging
import uuid
from typing import Any, Dict, List

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


async def get_roots_by_group(group_name: str) -> List[Dict[str, Any]]:
    roots = await dynamodb.async_query(
        TABLE_NAME,
        {
            'KeyConditionExpression': (
                Key('pk').eq(f'GROUP#{group_name}') &
                Key('sk').begins_with('ROOT#')
            ),
        }
    )

    if roots:
        return roots

    return []


async def add_root(group_name: str, root_attributes: Dict[str, Any]) -> None:
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
