# Standard libraries
import logging
import logging.config
from typing import (
    cast,
    Dict,
    List,
)

# Third-party libraries
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType,
    DynamoDelete as DynamoDeleteType,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'fi_project_comments'


async def add_comment(
    group_name: str,
    email: str,
    comment_data: CommentType
) -> bool:
    """ Add a comment in a group. """
    resp = False
    try:
        payload = {
            'project_name': group_name,
            'email': email
        }
        payload.update(cast(Dict[str, str], comment_data))
        resp = await dynamodb.async_put_item(TABLE_NAME, payload)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def delete_comment(group_name: str, user_id: str) -> bool:
    resp = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                'project_name': group_name,
                'user_id': user_id
            }
        )
        resp = await dynamodb.async_delete_item(TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def get_comments(group_name: str) -> List[Dict[str, str]]:
    """ Get comments of a group. """
    key_expression = Key('project_name').eq(group_name)
    query_attrs = {'KeyConditionExpression': key_expression}
    items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    return items
