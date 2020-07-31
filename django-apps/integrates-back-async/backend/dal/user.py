# Standard library
import logging
import contextlib
from typing import Dict, List, NamedTuple

# Third party libraries
from boto3.dynamodb.conditions import Attr, Key, Not
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb
from backend.typing import (
    DynamoDelete as DynamoDeleteType,
    User as UserType
)
from backend.utils import (
    apm,
)

# Local libraries
from __init__ import FI_TEST_PROJECTS


# Constants
LOGGER = logging.getLogger(__name__)

# Shared resources
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
ACCESS_TABLE = DYNAMODB_RESOURCE.Table('FI_project_access')
AUTHZ_TABLE = DYNAMODB_RESOURCE.Table('fi_authz')
USERS_TABLE = DYNAMODB_RESOURCE.Table('FI_users')
USERS_TABLE_NAME = 'FI_users'
AUTHZ_TABLE_NAME = 'fi_authz'

# Typing
SubjectPolicy = NamedTuple(
    'SubjectPolicy',
    [
        # interface for a row in fi_authz
        ('level', str),
        ('subject', str),
        ('object', str),
        ('role', str),
    ]
)


def cast_subject_policy_into_dict(policy: SubjectPolicy) -> dict:
    """Cast a subject policy into a dict, valid to be put in dynamo."""
    # pylint: disable=protected-access
    return {
        key: (
            value.lower()
            if isinstance(value, str)
            else value
        )
        for key, value in policy._asdict().items()
    }


def cast_dict_into_subject_policy(item: dict) -> SubjectPolicy:
    # pylint: disable=protected-access
    field_types: dict = SubjectPolicy._field_types

    # Every string as lowercase
    for field, _ in field_types.items():
        if isinstance(item.get(field), str):
            item[field] = item[field].lower()

    return SubjectPolicy(**{
        field: (
            item[field]
            if field in item and isinstance(item[field], typing)
            else typing()
        )
        for field, typing in field_types.items()
    })


def get_subject_policy(subject: str, object_: str) -> SubjectPolicy:
    """Return a policy for the given subject over the given object."""
    items = {}
    try:
        response = AUTHZ_TABLE.get_item(
            ConsistentRead=True,
            Key={
                'subject': subject.lower(),
                'object': object_.lower(),
            },
        )
        items = response.get('Item', {})
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return cast_dict_into_subject_policy(items)


def get_subject_policies(subject: str) -> List[SubjectPolicy]:
    """Return a list of policies for the given subject."""
    policies: List[SubjectPolicy] = []
    query_params = {
        'ConsistentRead': True,
        'KeyConditionExpression': Key('subject').eq(subject.lower()),
    }

    response = AUTHZ_TABLE.query(**query_params)
    policies.extend(map(cast_dict_into_subject_policy, response['Items']))

    while 'LastEvaluatedKey' in response:
        query_params['ExclusiveStartKey'] = response['LastEvaluatedKey']

        response = AUTHZ_TABLE.query(**query_params)
        policies.extend(map(cast_dict_into_subject_policy, response['Items']))

    return policies


async def put_subject_policy(policy: SubjectPolicy) -> bool:
    item = cast_subject_policy_into_dict(policy)

    with contextlib.suppress(ClientError):
        response = await dynamodb.async_put_item(AUTHZ_TABLE_NAME, item)
        return response

    LOGGER.error(
        'Error in user_dal.put_subject_policy',
        extra={'extra': locals()}
    )

    return False


async def delete_subject_policy(subject: str, object_: str) -> bool:
    with contextlib.suppress(ClientError):
        delete_attrs = DynamoDeleteType(
            Key={
                'subject': subject.lower(),
                'object': object_.lower(),
            }
        )
        response = await dynamodb.async_delete_item(
            AUTHZ_TABLE_NAME, delete_attrs
        )
        return response

    LOGGER.error(
        'Error in user_dal.delete_subject_policy',
        extra={'extra': locals()}
    )

    return False


def get_all(filter_exp: object, data_attr: str = '') -> List[Dict[str, str]]:
    scan_attrs = {}
    scan_attrs['FilterExpression'] = filter_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    response = USERS_TABLE.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = USERS_TABLE.scan(**scan_attrs)
        items += response['Items']

    return items


async def get_attributes(email: str, attributes: List[str]) -> UserType:
    items = {}
    try:
        query_attrs = {'KeyConditionExpression': Key('email').eq(email)}
        if attributes:
            projection = ','.join(attributes)
            query_attrs.update({'ProjectionExpression': projection})
        response_items = await dynamodb.async_query(
            USERS_TABLE_NAME, query_attrs
        )
        if response_items:
            items = response_items[0]
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return items


async def create(email: str, data: UserType) -> bool:
    resp = False

    try:
        data.update({'email': email})
        resp = await dynamodb.async_put_item(USERS_TABLE_NAME, data)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp


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
        success = await dynamodb.async_update_item(
            USERS_TABLE_NAME, update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success


def get(email: str) -> UserType:
    response = USERS_TABLE.get_item(Key={'email': email.lower()})
    return response.get('Item', {})


def delete(email: str) -> bool:
    primary_keys = {'email': email.lower()}
    resp = False
    try:
        item = USERS_TABLE.get_item(Key=primary_keys)
        if item.get('Item'):
            response = USERS_TABLE.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp


@apm.trace()
def get_projects(user_email: str, active: bool) -> List[str]:
    """ Get projects of a user """
    filtering_exp = Key('user_email').eq(user_email.lower())
    response = ACCESS_TABLE.query(KeyConditionExpression=filtering_exp)
    projects = response['Items']
    while response.get('LastEvaluatedKey'):
        response = ACCESS_TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        projects += response['Items']
    if active:
        projects_filtered = [
            project.get('project_name')
            for project in projects
            if project.get('has_access', '')
        ]
    else:
        projects_filtered = [
            project.get('project_name')
            for project in projects
            if not project.get('has_access', '')
        ]
    return projects_filtered


def get_platform_users() -> List[Dict[str, UserType]]:
    filter_exp = (
        Attr('has_access').eq(True) &
        Not(Attr('user_email').contains('@fluidattacks.com')) &
        Not(Attr('project_name').is_in(FI_TEST_PROJECTS.split(',')))
    )

    response = ACCESS_TABLE.scan(FilterExpression=filter_exp)
    users = response['Items']
    while response.get('LastEvaluatedKey'):
        response = ACCESS_TABLE.scan(
            FilterExpression=filter_exp,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        users += response['Items']

    return users
