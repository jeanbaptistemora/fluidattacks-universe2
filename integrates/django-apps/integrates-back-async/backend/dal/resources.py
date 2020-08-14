import logging
from typing import List
from botocore.exceptions import ClientError
from backend.dal.helpers import cloudfront, dynamodb, s3
from backend.dal import project as project_dal
from fluidintegrates.settings import LOGGING

from __init__ import (
    FI_AWS_S3_RESOURCES_BUCKET,
    FI_CLOUDFRONT_RESOURCES_DOMAIN
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def search_file(file_name: str) -> List[str]:
    return await s3.list_files(  # type: ignore
        FI_AWS_S3_RESOURCES_BUCKET,
        file_name
    )


async def save_file(file_object: object, file_name: str) -> bool:
    success: bool = await s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_RESOURCES_BUCKET,
        file_object,
        file_name
    )

    return success


async def remove_file(file_name: str) -> bool:
    return await s3.remove_file(  # type: ignore
        FI_AWS_S3_RESOURCES_BUCKET,
        file_name
    )


async def download_file(file_info: str, project_name: str) -> str:
    return await cloudfront.download_file(
        file_info,
        project_name,
        FI_CLOUDFRONT_RESOURCES_DOMAIN,
        1.0 / 6
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
