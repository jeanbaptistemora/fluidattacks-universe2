""" DAL functions for comments """

from __future__ import absolute_import

import boto3
from boto3.dynamodb.conditions import Attr, Key

# pylint:disable=relative-import
from __init__ import FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY


DYNAMODB_RESOURCE = boto3.resource(
    service_name='dynamodb',
    aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
    region_name='us-east-1')
TABLE = DYNAMODB_RESOURCE.Table('FI_comments')


def get_comments(comment_type, finding_id):
    """Get comments of the given finding"""
    key_exp = Key('finding_id').eq(finding_id)
    if comment_type == 'comment':
        filter_exp = Attr('comment_type').eq('comment') \
            | Attr('comment_type').eq('verification')
    elif comment_type == 'observation':
        filter_exp = Attr('comment_type').eq('observation')

    response = TABLE.query(
        FilterExpression=filter_exp, KeyConditionExpression=key_exp)
    comments = response.get('Items', [])
    while 'LastEvaluatedKey' in response:
        response = TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            FilterExpression=filter_exp,
            KeyConditionExpression=key_exp)
        comments += response.get('Items', [])

    return comments
