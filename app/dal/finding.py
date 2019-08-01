""" DAL functions for findings """

from __future__ import absolute_import

from boto3 import resource
from boto3.dynamodb.conditions import Key

# pylint:disable=relative-import
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY
)

DYNAMODB_RESOURCE = resource('dynamodb',
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
