from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils.group_comments import (
    format_group_comment_item,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_project_comments"


async def add_comment(
    group_name: str, email: str, comment_data: Dict[str, Any]
) -> bool:
    """Add a comment in a group."""
    resp = False
    try:
        payload = {"project_name": group_name, "email": email}
        payload.update(cast(Dict[str, str], comment_data))
        resp = await dynamodb_ops.put_item(TABLE_NAME, payload)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def add_comment_typed(comment_data: GroupComment) -> None:
    """Add a comment in a group."""
    comment_item = format_group_comment_item(comment_data)
    await add_comment(
        group_name=comment_data.group_name,
        email=comment_data.email,
        comment_data=comment_item,
    )


async def delete_comment(group_name: str, user_id: str) -> bool:
    resp = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={"project_name": group_name, "user_id": user_id}
        )
        resp = await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def get_comments(group_name: str) -> List[Dict[str, Any]]:
    """Get comments of a group."""
    key_expression = Key("project_name").eq(group_name)
    query_attrs = {"KeyConditionExpression": key_expression}
    items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    return items
