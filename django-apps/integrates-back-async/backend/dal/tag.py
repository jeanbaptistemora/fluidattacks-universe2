import logging
from decimal import Decimal
from typing import Dict, List, Optional, Union

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.dal.helpers import dynamodb
from backend.typing import (
    DynamoDelete as DynamoDeleteType,
    DynamoQuery as DynamoQueryType,
    Tag as TagType
)
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'fi_portfolios'


async def delete(organization: str, tag: str) -> bool:
    success: bool = False
    item = DynamoDeleteType(
        Key={
            'organization': organization.lower(),
            'tag': tag.lower()
        }
    )
    try:
        success = await dynamodb.async_delete_item(TABLE_NAME, item)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def update(
        organization: str,
        tag: str,
        data: Dict[str, Union[List[str], Decimal]]) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_names = {}
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'#{attr}, '
            expression_names.update({f'#{attr}': attr})
        else:
            set_expression += f'#{attr} = :{attr}, '
            expression_names.update({f'#{attr}': attr})
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'
    update_attrs = {
        'Key': {
            'organization': organization,
            'tag': tag
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }

    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    if expression_names:
        update_attrs.update({'ExpressionAttributeNames': expression_names})
    try:
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def get_attributes(
        organization: str,
        tag: str,
        attributes: List[str]) -> Dict[str, Union[List[str], str]]:
    response = {}
    item_attrs: DynamoQueryType = {
        'KeyConditionExpression': (
            Key('organization').eq(organization.lower()) &
            Key('tag').eq(tag.lower())
        ),
        'ProjectionExpression': ','.join(attributes)
    }
    response_items = await dynamodb.async_query(TABLE_NAME, item_attrs)
    if response_items:
        response = response_items[0]
    return response


async def get_tags(
        organization: str,
        attributes: Optional[List[str]]) -> List[TagType]:
    tags: List[TagType] = []

    query_attrs = {
        'KeyConditionExpression': Key('organization').eq(organization)
    }
    if attributes:
        projection = ','.join(attributes)
        query_attrs.update({'ProjectionExpression': projection})

    try:
        tags = await dynamodb.async_query(TABLE_NAME, query_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return tags
