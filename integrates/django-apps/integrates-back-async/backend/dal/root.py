# Standard
from typing import Any, Dict, List

# Third party
from boto3.dynamodb.conditions import Key

# Local
from backend.dal.helpers import dynamodb


# Constants
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
