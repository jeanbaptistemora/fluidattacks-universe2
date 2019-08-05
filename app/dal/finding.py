""" DAL functions for findings """

from __future__ import absolute_import

import boto3
from boto3.dynamodb.conditions import Key

# pylint:disable=relative-import
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY
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
    success = s3.upload_memory_file(file_object, file_name)

    return success
