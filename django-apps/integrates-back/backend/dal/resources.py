
from typing import Dict, List, Union
from botocore.exceptions import ClientError
import rollbar
from backend.dal.helpers import dynamodb, s3
from backend.dal import project as project_dal

from __init__ import FI_AWS_S3_RESOURCES_BUCKET

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')

ResourceType = Dict[str, Union[str, List[Dict[str, str]]]]


def search_file(file_name: str) -> List[str]:
    return s3.list_files(FI_AWS_S3_RESOURCES_BUCKET, file_name)  # type: ignore


def save_file(file_object: object, file_name: str) -> bool:
    success = s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_RESOURCES_BUCKET, file_object, file_name)

    return success


def remove_file(file_name: str) -> bool:
    return s3.remove_file(FI_AWS_S3_RESOURCES_BUCKET, file_name)  # type: ignore


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
            if attr_name not in item[0]:
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
                UpdateExpression='SET #attrName = list_append(#attrName, :val1)',
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


def remove(project_name: str, res_type: str, index: int) -> bool:
    table = TABLE
    table_name = 'FI_projects'
    primary_name_key = 'project_name'
    primary_key = project_name
    attr_name = res_type
    table = DYNAMODB_RESOURCE.Table(table_name)
    resp = False
    try:
        response = table.update_item(
            Key={
                primary_name_key: primary_key.lower(),
            },
            UpdateExpression='REMOVE #attrName[' + str(index) + ']',
            ExpressionAttributeNames={
                '#attrName': attr_name
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def update(res_data: List[Dict[str, Union[str, List[str], object]]],
           project_name: str, res_type: str) -> bool:
    table = TABLE
    primary_keys = ['project_name', project_name]
    attr_name = res_type
    item = project_dal.get(project_name)
    resp = False
    try:
        if attr_name not in item[0]:
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
