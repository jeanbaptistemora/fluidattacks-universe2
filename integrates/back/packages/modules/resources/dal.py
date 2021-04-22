import logging
import logging.config

from botocore.exceptions import ClientError

from back.settings import LOGGING
from dynamodb import operations_legacy as dynamodb_ops


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_projects'


async def remove(group_name: str, res_type: str, index: int) -> bool:
    resp = False
    try:
        update_attrs = {
            'Key': {'project_name': group_name.lower()},
            'UpdateExpression': 'REMOVE #attrName[' + str(index) + ']',
            'ExpressionAttributeNames': {'#attrName': res_type}
        }
        resp = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp
