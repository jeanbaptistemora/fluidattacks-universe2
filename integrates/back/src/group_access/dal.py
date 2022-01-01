from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
    Group as GroupType,
    GroupAccess as GroupAccessType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
import newrelic.agent
from newutils import (
    datetime as datetime_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from typing import (
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_project_access"


async def get_access_by_url_token(
    url_token: str,
) -> List[Dict[str, GroupType]]:
    """Get user access of a group by the url token"""
    filter_exp = Attr("invitation").exists() & Attr("invitation.url_token").eq(
        url_token
    )
    scan_attrs = {"FilterExpression": filter_exp}
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return items


async def get_group_users(group: str, active: bool = True) -> List[str]:
    """Get users of a group."""
    group_name = group.lower()
    key_condition = Key("project_name").eq(group_name)
    projection_expression = (
        "user_email, has_access, project_name, responsibility"
    )
    now_epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())
    filter_exp = Attr("expiration_time").not_exists() | Attr(
        "expiration_time"
    ).gt(now_epoch)
    query_attrs = {
        "IndexName": "project_access_users",
        "KeyConditionExpression": key_condition,
        "ProjectionExpression": projection_expression,
        "FilterExpression": filter_exp,
    }
    users = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if active:
        users_filtered = [
            user.get("user_email")
            for user in users
            if user.get("has_access", "")
        ]
    else:
        users_filtered = [
            user.get("user_email")
            for user in users
            if not user.get("has_access", "")
        ]
    return users_filtered


async def get_user_access(
    user_email: str, group_name: str
) -> List[Dict[str, GroupType]]:
    """Get user access of a group"""
    user_email = user_email.lower()
    group_name = group_name.lower()
    filter_key = "user_email"
    filter_sort = "project_name"
    filtering_exp = Key(filter_key).eq(user_email) & Key(filter_sort).eq(
        group_name
    )
    query_attrs = {"KeyConditionExpression": filtering_exp}
    items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    return items


@newrelic.agent.function_trace()
async def get_user_groups(user_email: str, active: bool) -> List[str]:
    """Get groups of a user"""
    filtering_exp = Key("user_email").eq(user_email.lower())
    query_attrs = {"KeyConditionExpression": filtering_exp}
    groups = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if active:
        groups_filtered = [
            get_key_or_fallback(group)
            for group in groups
            if group.get("has_access", "")
        ]
    else:
        groups_filtered = [
            get_key_or_fallback(group)
            for group in groups
            if not group.get("has_access", "")
        ]
    return groups_filtered


async def remove_access(user_email: str, group_name: str) -> bool:
    """Remove group access in dynamo."""
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                "user_email": user_email.lower(),
                "project_name": group_name.lower(),
            }
        )
        resp = await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs)
        return resp
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return False


async def update(
    user_email: str, group_name: str, data: GroupAccessType
) -> bool:
    """Update group access attributes."""
    success = False
    set_expression = ""
    remove_expression = ""
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"{attr}, "
        else:
            set_expression += f"{attr} = :{attr}, "
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {
            "user_email": user_email.lower(),
            "project_name": group_name.lower(),
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success
