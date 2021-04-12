# Standard libraries
import logging
import logging.config

# Third-party libraries
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import ProjectAccess as GroupAccessType


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_project_access'


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
