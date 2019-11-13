"""DAL functions for findings."""

import rollbar
from botocore.exceptions import ClientError

# pylint:disable=relative-import
from __init__ import FI_AWS_S3_BUCKET
from app.dal.helpers import s3, dynamodb


DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
TABLE = DYNAMODB_RESOURCE.Table('FI_findings')


def create(finding_id, project_name, finding_attrs):
    success = False
    try:
        finding_attrs.update({
            'finding_id': finding_id,
            'project_name': project_name
        })
        response = TABLE.put_item(Item=finding_attrs)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create draft',
                               'error', extra_data=ex, payload_data=locals())
    return success


def update(finding_id, data):
    success = False
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key={'finding_id': finding_id},
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = ['{attr} = :{attr}'.format(attr=attr) for attr in data]
            values = {':{}'.format(attr): data[attr] for attr in data}

            response = TABLE.update_item(
                Key={'finding_id': finding_id},
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt update finding',
                               'error', extra_data=ex, payload_data=locals())

    return success


def delete(finding_id):
    success = False
    try:
        response = TABLE.delete_item(Key={'finding_id': finding_id})
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt delete finding',
                               'error', extra_data=ex, payload_data=locals())

    return success


def get_finding(finding_id):
    """ Retrieve all attributes from a finding """
    response = TABLE.get_item(Key={'finding_id': finding_id})

    return response.get('Item', {})


def save_evidence(file_object, file_name):
    success = s3.upload_memory_file(FI_AWS_S3_BUCKET, file_object, file_name)

    return success


def search_evidence(file_name):
    return s3.list_files(FI_AWS_S3_BUCKET, file_name)


def remove_evidence(file_name):
    return s3.remove_file(FI_AWS_S3_BUCKET, file_name)


def download_evidence(file_name, file_path):
    s3.download_file(FI_AWS_S3_BUCKET, file_name, file_path)
