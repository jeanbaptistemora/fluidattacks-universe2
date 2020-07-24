
from typing import List, Union
from asgiref.sync import async_to_sync
from botocore.exceptions import ClientError
import rollbar
from backend.dal.helpers import cloudfront, dynamodb, s3
from backend.typing import Resource as ResourceType
from backend.dal import project as project_dal
from backend.utils import logging

from __init__ import (
    FI_AWS_S3_RESOURCES_BUCKET,
    FI_CLOUDFRONT_RESOURCES_DOMAIN
)

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')


@async_to_sync
async def search_file(file_name: str) -> List[str]:
    return await s3.list_files(  # type: ignore
        FI_AWS_S3_RESOURCES_BUCKET,
        file_name
    )


async def save_file(file_object: object, file_name: str) -> bool:
    success = await s3.upload_memory_file(  # type: ignore
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


@async_to_sync
async def download_file(file_info: str, project_name: str) -> str:
    return await cloudfront.download_file(
        file_info,
        project_name,
        FI_CLOUDFRONT_RESOURCES_DOMAIN,
        1.0 / 6
    )


def create(res_data: Union[List[ResourceType], ResourceType],
           project_name: str, res_type: str) -> bool:
    table = TABLE
    primary_name_key = 'project_name'
    primary_key = project_name
    attr_name = res_type
    item = project_dal.get(project_name)
    primary_key = primary_key.lower()
    resp = False
    try:
        if not item:
            response = table.put_item(
                Item={
                    primary_name_key: primary_key,
                    attr_name: res_data,
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        else:
            if attr_name not in item:
                table.update_item(
                    Key={
                        primary_name_key: primary_key,
                    },
                    UpdateExpression='SET #attrName = :val1',
                    ExpressionAttributeNames={
                        '#attrName': attr_name
                    },
                    ExpressionAttributeValues={
                        ':val1': []
                    }
                )
            update_response = table.update_item(
                Key={
                    primary_name_key: primary_key,
                },
                UpdateExpression=(
                    'SET #attrName = list_append(#attrName, :val1)'
                ),
                ExpressionAttributeNames={
                    '#attrName': attr_name
                },
                ExpressionAttributeValues={
                    ':val1': res_data
                }
            )
            resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


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
        logging.log(ex, 'error', extra=locals())
    return resp


def update(res_data: List[ResourceType],
           project_name: str, res_type: str) -> bool:
    table = TABLE
    primary_keys = ['project_name', project_name]
    attr_name = res_type
    item = project_dal.get(project_name)
    resp = False
    try:
        if attr_name not in item:
            table.update_item(
                Key={
                    primary_keys[0]: primary_keys[1]
                },
                UpdateExpression='SET #attrName = :val1',
                ExpressionAttributeNames={
                    '#attrName': attr_name
                },
                ExpressionAttributeValues={
                    ':val1': []
                }
            )
        update_response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1],
            },
            UpdateExpression='SET #attrName = :val1',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': res_data
            }
        )
        resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp
