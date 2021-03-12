import logging
import logging.config
from typing import List

from botocore.exceptions import ClientError

from back.settings import LOGGING
from backend.dal import project as project_dal
from backend.dal.helpers import (
    dynamodb,
    s3,
)
from __init__ import (
    FI_AWS_S3_RESOURCES_BUCKET,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def download_file(file_info: str, project_name: str) -> str:
    project_name = project_name.lower()
    file_url = project_name + '/' + file_info
    return await s3.sign_url(
        file_url,
        10,
        FI_AWS_S3_RESOURCES_BUCKET
    )


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


async def remove_file(file_name: str) -> bool:
    return await s3.remove_file(
        FI_AWS_S3_RESOURCES_BUCKET,
        file_name
    )


async def save_file(file_object: object, file_name: str) -> bool:
    success: bool = await s3.upload_memory_file(
        FI_AWS_S3_RESOURCES_BUCKET,
        file_object,
        file_name
    )
    return success


async def search_file(file_name: str) -> List[str]:
    return await s3.list_files(
        FI_AWS_S3_RESOURCES_BUCKET,
        file_name
    )
