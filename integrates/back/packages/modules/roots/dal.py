# Standard
from typing import Any, Dict, Tuple

# Third party
from boto3.dynamodb.conditions import Key

# Local
from backend.dal.helpers import dynamodb
from backend.model import dynamo_model


# Constants
ENTITY = 'ROOT'
TABLE_NAME = 'integrates_vms'


async def get_roots(group_name: str) -> Tuple[Dict[str, Any], ...]:
    primary_key = dynamo_model.build_key(
        entity=ENTITY,
        partition_key=group_name,
        sort_key=''
    )

    results = await dynamodb.async_query(
        TABLE_NAME,
        {
            'IndexName': 'inverted_index',
            'KeyConditionExpression': (
                Key('sk').eq(primary_key.partition_key) &
                Key('pk').begins_with(primary_key.sort_key)
            )
        }
    )

    return tuple(results)
