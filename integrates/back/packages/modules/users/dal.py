
import logging
import logging.config
from typing import (
    Dict,
    List,
)

from boto3.dynamodb.conditions import (
    Attr,
    Key,
    Not,
)
from botocore.exceptions import ClientError

from __init__ import FI_TEST_PROJECTS
from back.settings import LOGGING
from custom_exceptions import UnavailabilityError
from custom_types import (
    DynamoDelete as DynamoDeleteType,
    User as UserType,
)
from dynamodb import operations_legacy as dynamodb_ops


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)

# Shared resources
ACCESS_TABLE_NAME = 'FI_project_access'
USERS_TABLE_NAME = 'FI_users'


async def create(email: str, data: UserType) -> bool:
    resp = False
    try:
        data.update({'email': email})
        resp = await dynamodb_ops.put_item(USERS_TABLE_NAME, data)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return resp


async def delete(email: str) -> bool:
    resp = False
    try:
        delete_attrs = DynamoDeleteType(Key={'email': email.lower()})
        resp = await dynamodb_ops.delete_item(USERS_TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp


async def get(email: str) -> UserType:
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('email').eq(email.lower()),
        'Limit': 1
    }
    response_items = await dynamodb_ops.query(USERS_TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]
    return response


async def get_all(
    filter_exp: object,
    data_attr: str = ''
) -> List[Dict[str, UserType]]:
    scan_attrs = {}
    scan_attrs['FilterExpression'] = filter_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    items = await dynamodb_ops.scan(USERS_TABLE_NAME, scan_attrs)
    return items


async def get_attributes(email: str, attributes: List[str]) -> UserType:
    items = {}
    try:
        query_attrs = {'KeyConditionExpression': Key('email').eq(email)}
        if attributes:
            projection = ','.join(attributes)
            query_attrs.update({'ProjectionExpression': projection})
        response_items = await dynamodb_ops.query(
            USERS_TABLE_NAME, query_attrs
        )
        if response_items:
            items = response_items[0]
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return items


async def get_platform_users() -> List[Dict[str, UserType]]:
    filter_exp = (
        Attr('has_access').eq(True) &
        Not(Attr('user_email').contains('@fluidattacks.com')) &
        Not(Attr('project_name').is_in(FI_TEST_PROJECTS.split(',')))
    )
    scan_attrs = {'FilterExpression': filter_exp}
    return await dynamodb_ops.scan(ACCESS_TABLE_NAME, scan_attrs)


async def update(email: str, data: UserType) -> bool:
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
        'Key': {'email': email.lower()},
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    if expression_names:
        update_attrs.update({'ExpressionAttributeNames': expression_names})
    try:
        success = await dynamodb_ops.update_item(
            USERS_TABLE_NAME, update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
