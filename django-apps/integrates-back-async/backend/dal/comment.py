"""DAL functions for comments."""

from typing import List
import rollbar
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from backend.dal.helpers import dynamodb
from backend.typing import Comment as CommentType

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_comments')
TABLE_NAME: str = 'FI_comments'


async def create(comment_id: int, comment_attributes: CommentType) -> bool:
    success = False
    try:
        comment_attributes.update({'user_id': comment_id})
        success = await dynamodb.async_put_item(
            TABLE_NAME, comment_attributes
        )
    except ClientError as ex:
        rollbar.report_message(
            'Error: Couldn\'nt create comment',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return success


def delete(finding_id, user_id) -> bool:
    resp = False
    try:
        response = TABLE.delete_item(
            Key={
                'finding_id': finding_id,
                'user_id': user_id
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


async def get_comments(
        comment_type: str,
        finding_id: int) -> List[CommentType]:
    """Get comments of the given finding"""
    key_exp = Key('finding_id').eq(finding_id)
    comment_type = comment_type.lower()
    if comment_type == 'comment':
        filter_exp: object = Attr('comment_type').eq('comment') \
            | Attr('comment_type').eq('verification')
    elif comment_type == 'observation':
        filter_exp = Attr('comment_type').eq('observation')
    elif comment_type == 'event':
        filter_exp = Attr('comment_type').eq('event')

    query_attrs = {
        'KeyConditionExpression': key_exp,
        'FilterExpression': filter_exp
    }
    return await dynamodb.async_query(TABLE_NAME, query_attrs)
