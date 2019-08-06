""" DAL functions for findings """

from __future__ import absolute_import

import boto3
from boto3.dynamodb.conditions import Key

# pylint:disable=relative-import
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY, FI_AWS_S3_BUCKET
)
from app.dal.helpers import s3


DYNAMODB_RESOURCE = boto3.resource(
    service_name='dynamodb',
    aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
    region_name='us-east-1')
TABLE = DYNAMODB_RESOURCE.Table('FI_findings')


def get_finding(finding_id):
    """ Retrieve all attributes from a finding """

    filtering_exp = Key('finding_id').eq(finding_id)
    response = TABLE.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE.query(KeyConditionExpression=filtering_exp,
                               ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']

    return items[0] if items else {}


def save_evidence(file_object, file_name):
    success = s3.upload_memory_file(FI_AWS_S3_BUCKET, file_object, file_name)

    return success


def migrate_evidence(file_path, file_name):
    success = s3.upload_stored_file(FI_AWS_S3_BUCKET, file_path, file_name)

    return success


def search_evidence(file_name):
    return s3.list_files(FI_AWS_S3_BUCKET, file_name)


def remove_evidence(file_name):
    return s3.remove_file(FI_AWS_S3_BUCKET, file_name)


def download_evidence(file_name, file_path):
    s3.download_file(FI_AWS_S3_BUCKET, file_name, file_path)
