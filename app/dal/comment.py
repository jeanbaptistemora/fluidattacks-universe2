"""DAL functions for comments."""

from boto3.dynamodb.conditions import Attr, Key

from app.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
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
