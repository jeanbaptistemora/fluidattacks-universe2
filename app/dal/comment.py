"""DAL functions for comments."""

import rollbar
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from app.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
TABLE = DYNAMODB_RESOURCE.Table('FI_comments')


def create(comment_id, comment_attributes):
    success = False
    try:
        comment_attributes.update({'user_id': comment_id})
        response = TABLE.put_item(Item=comment_attributes)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create comment',
                               'error', extra_data=ex, payload_data=locals())
    return success


def get_comments(comment_type, finding_id):
    """Get comments of the given finding"""
    key_exp = Key('finding_id').eq(finding_id)
    if comment_type == 'comment':
        filter_exp = Attr('comment_type').eq('comment') \
            | Attr('comment_type').eq('verification')
    elif comment_type == 'observation':
        filter_exp = Attr('comment_type').eq('observation')
    elif comment_type == 'event':
        filter_exp = Attr('comment_type').eq('event')

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
