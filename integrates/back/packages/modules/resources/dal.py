import logging
import logging.config

from botocore.exceptions import ClientError

from back.settings import LOGGING
from backend.dal import project as project_dal
from backend.dal.helpers import dynamodb


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def remove(project_name: str, res_type: str, index: int) -> bool:
    resp = False
    try:
        update_attrs = {
            'Key': {'project_name': project_name.lower()},
            'UpdateExpression': 'REMOVE #attrName[' + str(index) + ']',
            'ExpressionAttributeNames': {
                '#attrName': res_type
            }
        }
        resp = await dynamodb.async_update_item(
            project_dal.TABLE_NAME,
            update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp
