"""DAL functions for comments."""
import logging
from typing import List

from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType,
    DynamoDelete as DynamoDeleteType
)
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_comments'


async def create(comment_id: int, comment_attributes: CommentType) -> bool:
    success = False
    try:
        comment_attributes.update({'user_id': comment_id})
        success = await dynamodb.async_put_item(
            TABLE_NAME, comment_attributes
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def delete(finding_id: int, user_id: int) -> bool:
    success = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                'finding_id': finding_id,
                'user_id': user_id
            }
        )
        success = await dynamodb.async_delete_item(TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success


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
    elif comment_type == 'zero_risk':
        filter_exp = Attr('comment_type').eq('zero_risk')

    query_attrs = {
        'KeyConditionExpression': key_exp,
        'FilterExpression': filter_exp
    }
    return await dynamodb.async_query(TABLE_NAME, query_attrs)


async def edit_scope(
    comment_id: int,
    comment_scope: str,
    element_id: int,
) -> bool:
    """Edit the scope (internal/external) on the given comment"""
    success = False
    try:
        expression_values = {':cs': comment_scope}

        edited_scope = {
            'Key': {
                'finding_id': element_id,
                'user_id': comment_id
            },
            'UpdateExpression': 'SET comment_scope = :cs',
            'ExpressionAttributeValues': expression_values,
            'ConditionExpression':
                Attr('user_id').exists() & Attr('finding_id').exists()
        }
        success = await dynamodb.async_update_item(TABLE_NAME, edited_scope)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success
