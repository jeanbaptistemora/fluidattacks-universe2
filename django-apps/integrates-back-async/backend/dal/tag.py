import logging
from decimal import Decimal
from typing import Dict, List, Optional, Union

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.dal.helpers import dynamodb
from backend.typing import (
    DynamoDelete as DynamoDeleteType,
    Tag as TagType
)

# Constants
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'fi_portfolios'
TABLE = DYNAMODB_RESOURCE.Table(TABLE_NAME)


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


def update(organization: str, tag: str,
           data: Dict[str, Union[List[str], Decimal]]) -> bool:
    success = False
    primary_keys = {
        'organization': organization,
        'tag': tag
    }
    try:
        attrs_to_remove = [
            attr
            for attr in data
            if data[attr] is None
        ]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = [
                f'{attr} = :{attr}'
                for attr in data
            ]
            values = {
                ':{}'.format(attr): data[attr]
                for attr in data
            }

            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='SET ' + ','.join(attributes),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


def get_attributes(organization: str, tag: str,
                   attributes: List[str]) -> Dict[str, Union[List[str], str]]:
    item_attrs: Dict[str, Union[List[str], Dict[str, str]]] = {
        'Key': {
            'organization': organization.lower(),
            'tag': tag.lower()
        },
        'AttributesToGet': attributes
    }
    response = TABLE.get_item(**item_attrs)
    return response.get('Item', {})


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
