# Standard libraries
import logging
import logging.config
from typing import List

# Third-party libraries
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import (
    DynamoDelete as DynamoDeleteType,
    ProjectAccess as GroupAccessType,
)
from newutils import apm


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_project_access'


@apm.trace()
async def get_user_groups(user_email: str, active: bool) -> List[str]:
    """ Get groups of a user """
    filtering_exp = Key('user_email').eq(user_email.lower())
    query_attrs = {'KeyConditionExpression': filtering_exp}
    groups = await dynamodb.async_query(TABLE_NAME, query_attrs)
    if active:
        groups_filtered = [
            group.get('project_name')
            for group in groups
            if group.get('has_access', '')
        ]
    else:
        groups_filtered = [
            group.get('project_name')
            for group in groups
            if not group.get('has_access', '')
        ]
    return groups_filtered


async def remove_access(user_email: str, group_name: str) -> bool:
    """Remove group access in dynamo."""
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                'user_email': user_email.lower(),
                'project_name': group_name.lower(),
            }
        )
        resp = await dynamodb.async_delete_item(TABLE_NAME, delete_attrs)
        return resp
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return False


async def update(
    user_email: str,
    group_name: str,
    data: GroupAccessType
) -> bool:
    """Update group access attributes."""
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {
            'user_email': user_email.lower(),
            'project_name': group_name.lower()
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(
            TABLE_NAME,
            update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
