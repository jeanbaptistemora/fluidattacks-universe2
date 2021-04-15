# Standard libraries
from typing import (
    Dict,
    List,
)

# Third-party libraries
from boto3.dynamodb.conditions import Key

# Local libraries
from backend.dal.helpers import dynamodb


# Constants
TABLE_NAME: str = 'fi_project_comments'


async def get_comments(group_name: str) -> List[Dict[str, str]]:
    """ Get comments of a group. """
    key_expression = Key('project_name').eq(group_name)
    query_attrs = {'KeyConditionExpression': key_expression}
    items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    return items
