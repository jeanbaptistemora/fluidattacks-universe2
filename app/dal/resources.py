
# pylint:disable=relative-import
from botocore.exceptions import ClientError
import rollbar
from __init__ import FI_AWS_S3_RESOURCES_BUCKET
from app.dal.helpers import dynamodb, s3
from app.dal import integrates_dal


DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')


def search_file(file_name):
    return s3.list_files(FI_AWS_S3_RESOURCES_BUCKET, file_name)


def save_file(file_object, file_name):
    success = s3.upload_memory_file(
        FI_AWS_S3_RESOURCES_BUCKET, file_object, file_name)

    return success


def remove_file(file_name):
    return s3.remove_file(FI_AWS_S3_RESOURCES_BUCKET, file_name)


def update(res_data, project_name, res_type):
    table = TABLE
    table_name = 'FI_projects'
    primary_keys = ['project_name', project_name]
    attr_name = res_type
    item = integrates_dal.get_data_dynamo(table_name, primary_keys[0], primary_keys[1])
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
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False
