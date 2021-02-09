"""DAL functions for projects."""

import logging
from typing import (
    Any,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
    Union,
)

import aioboto3
from aioextensions import collect
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key

from backend import authz
from backend.dal.event import TABLE_NAME as EVENTS_TABLE_NAME
from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType,
    DynamoDelete as DynamoDeleteType,
    Project as ProjectType,
    ProjectAccess as ProjectAccessType,
)
from backend.dal.user import get_user_name
from back.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_ACCESS_NAME = 'FI_project_access'
TABLE_NAME = 'FI_projects'
TABLE_GROUP_COMMENTS = 'fi_project_comments'

ServicePolicy = NamedTuple(
    'ServicePolicy',
    [('group', str), ('service', str)]
)


async def get_service_policies(group: str) -> List[ServicePolicy]:
    """Return a list of policies for the given group."""
    policies: List[ServicePolicy] = []

    query_attrs = {
        'KeyConditionExpression': Key('project_name').eq(group.lower()),
        'ConsistentRead': True,
        'ProjectionExpression': 'historic_configuration, project_status'
    }
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)

    # There is no such group, let's make an early return
    if not response_items:
        return policies

    group_attributes = response_items[0]

    historic_config: List[Dict[str, Any]] = group_attributes[
        'historic_configuration'
    ]

    has_drills: bool = historic_config[-1]['has_drills']
    has_forces: bool = historic_config[-1]['has_forces']
    has_integrates: bool = group_attributes['project_status'] == 'ACTIVE'
    type_: str = historic_config[-1]['type']

    if type_ == 'continuous':

        policies.append(
            ServicePolicy(group=group, service='continuous')
        )
        if has_integrates:
            policies.append(
                ServicePolicy(group=group, service='integrates')
            )

            if has_drills:
                policies.append(
                    ServicePolicy(group=group, service='drills_white')
                )

                if has_forces:
                    policies.append(
                        ServicePolicy(group=group, service='forces')
                    )

    elif type_ == 'oneshot':

        if has_integrates:
            policies.append(
                ServicePolicy(group=group, service='integrates')
            )
            policies.append(
                ServicePolicy(group=group, service='drills_black')
            )

    else:
        LOGGER.critical(
            'Group has invalid type attribute',
            extra={'extra': dict(group=group)})

    return policies


async def get_active_projects() -> List[str]:
    """Get active project in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') &
        Attr('project_status').exists()
    )
    projects = await get_all(filtering_exp, 'project_name')
    return cast(
        List[str],
        [prj['project_name'] for prj in projects]
    )


async def get_projects_with_forces() -> List[str]:
    """Get active project in DynamoDB"""
    query_attrs = {
        "ProjectionExpression": "#name,#h_config",
        "ExpressionAttributeNames": {
            "#name": "project_name",
            "#h_config": "historic_configuration",
        },
    }
    response = await dynamodb.async_scan(TABLE_NAME, query_attrs)
    projects = [
        project['project_name'] for project in response
        if project['historic_configuration'][-1]['has_forces']
    ]

    return cast(List[str], projects)


async def get_alive_projects() -> List[str]:
    """Get active and suspended projects in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') |
        Attr('project_status').eq('SUSPENDED')
    )
    projects = await get_all(filtering_exp, 'project_name')
    return cast(
        List[str],
        [prj['project_name'] for prj in projects]
    )


async def get_group(
        group_name: str,
        table: aioboto3.session.Session.client) -> ProjectType:
    response = await table.get_item(Key={'project_name': group_name})
    return response.get('Item', {})


async def list_events(project_name: str) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    query_attrs = {
        'KeyConditionExpression': key_exp,
        'IndexName': 'project_events',
        'ProjectionExpression': 'event_id'
    }
    events = await dynamodb.async_query(EVENTS_TABLE_NAME, query_attrs)

    return [event['event_id'] for event in events]


async def list_internal_managers(project_name: str) -> List[str]:
    all_managers = await list_project_managers(project_name)
    internal_managers = [
        user
        for user in all_managers
        if user.endswith('@fluidattacks.com')
    ]
    return internal_managers


async def get_description(project: str) -> str:
    """ Get the description of a project. """
    description = await get_attributes(project, ['description'])
    project_description = ''
    if description:
        project_description = str(description.get('description', ''))
    else:
        # project without description
        pass
    return project_description


async def get_users(project: str, active: bool = True) -> List[str]:
    """Get users of a project."""
    project_name = project.lower()
    key_condition = Key('project_name').eq(project_name)
    projection_expression = \
        'user_email, has_access, project_name, responsibility'
    query_attrs = {
        'IndexName': 'project_access_users',
        'KeyConditionExpression': key_condition,
        'ProjectionExpression': projection_expression
    }
    users = await dynamodb.async_query(TABLE_ACCESS_NAME, query_attrs)
    if active:
        users_filtered = [
            user.get('user_email')
            for user in users
            if user.get('has_access', '')
        ]
    else:
        users_filtered = [
            user.get('user_email')
            for user in users
            if not user.get('has_access', '')
        ]
    return users_filtered


async def exists(
    project_name: str,
    pre_computed_project_data: Optional[Dict[str, str]] = None
) -> bool:
    project = project_name.lower()
    project_data = (
        pre_computed_project_data or
        await get_attributes(project, ['project_name'])
    )

    return bool(project_data)


async def list_project_managers(group: str) -> List[str]:
    users_active, users_inactive = await collect([
        get_users(group, True),
        get_users(group, False)
    ])
    all_users = users_active + users_inactive
    users_roles = await collect([
        authz.get_group_level_role(user, group)
        for user in all_users
    ])
    managers = [
        user
        for user, role in zip(all_users, users_roles)
        if role == 'group_manager'
    ]
    return managers


async def get_attributes(
    project_name: str,
    attributes: Optional[List[str]] = None,
    table: aioboto3.session.Session.client = None
) -> Dict[str, Union[str, List[str]]]:
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('project_name').eq(project_name),
        'Limit': 1
    }
    if attributes:
        projection = ','.join(attributes)
        query_attrs.update({'ProjectionExpression': projection})

    if not table:
        response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    else:
        response_item = await table.query(**query_attrs)
        response_items = response_item.get('Items', [])

    if response_items:
        response = response_items[0]

    return response


async def is_alive(
    project: str,
    pre_computed_project_data: Optional[Dict[str, Any]] = None
) -> bool:
    """Validate if a project exist and is not deleted."""
    project_name = project.lower()
    is_valid_project = True
    if await exists(project_name, pre_computed_project_data):
        project_data = (
            pre_computed_project_data or
            await get_attributes(
                project_name.lower(),
                ['deletion_date', 'project_status']
            )
        )
        if project_data.get('project_status') != 'ACTIVE' or \
           project_data.get('deletion_date'):
            is_valid_project = False
    else:
        is_valid_project = False
    return is_valid_project


async def can_user_access(
        project: str,
        role: str,
        table: aioboto3.session.Session.client = None) -> bool:
    project_data = await get_attributes(
        project.lower(),
        [
            'deletion_date',
            'historic_deletion',
            'project_name',
            'project_status',
        ],
        table
    )

    is_user_allowed = False
    if await is_alive(project, project_data):
        is_user_allowed = bool(role)
    return is_user_allowed


async def update(project_name: str, data: ProjectType) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {'project_name': project_name.lower()},
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
        # By default updates on non-existent items create a new item
        # This condition disables that effect
        'ConditionExpression': Attr('project_name').exists(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success


async def create(project: ProjectType) -> bool:
    """Add project to dynamo."""
    resp = False
    try:
        resp = await dynamodb.async_put_item(TABLE_NAME, project)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return resp


async def add_comment(
        project_name: str,
        email: str,
        comment_data: CommentType) -> bool:
    """ Add a comment in a project. """
    resp = False
    try:
        payload = {
            'project_name': project_name,
            'email': email
        }
        payload.update(cast(Dict[str, str], comment_data))
        resp = await dynamodb.async_put_item(TABLE_GROUP_COMMENTS, payload)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def get_comments(project_name: str) -> List[Dict[str, str]]:
    """ Get comments of a project. """
    key_expression = Key('project_name').eq(project_name)
    query_attrs = {
        'KeyConditionExpression': key_expression
    }
    items = await dynamodb.async_query(TABLE_GROUP_COMMENTS, query_attrs)
    comment_name_data = await collect([
        get_user_name(mail)
        for mail in set(item['email'] for item in items)
    ])
    comment_fullnames = {
        mail: list(fullnames.values())
        for data in comment_name_data for mail, fullnames in data.items()
    }

    for item in items:
        item['fullname'] = ' '.join(
            filter(None, comment_fullnames[item['email']][::-1])
        )
    return items


async def delete_comment(group_name: str, user_id: str) -> bool:
    resp = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                'project_name': group_name,
                'user_id': user_id
            }
        )
        resp = await dynamodb.async_delete_item(
            TABLE_GROUP_COMMENTS, delete_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def get_all(
        filtering_exp: object = '', data_attr: str = '') -> List[ProjectType]:
    """Get all projects"""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs['FilterExpression'] = filtering_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr

    async with aioboto3.resource(**dynamodb.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(TABLE_NAME)
        response = await table.scan(**scan_attrs)
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = await table.scan(**scan_attrs)
            items += response.get('Items', [])

    return cast(List[ProjectType], items)


async def get_user_access(
        user_email: str,
        project_name: str) -> List[Dict[str, ProjectType]]:
    """Get user access of a project."""
    user_email = user_email.lower()
    project_name = project_name.lower()
    filter_key = 'user_email'
    filter_sort = 'project_name'
    filtering_exp = (
        Key(filter_key).eq(user_email) &
        Key(filter_sort).eq(project_name)
    )
    query_attrs = {
        'KeyConditionExpression': filtering_exp
    }
    items = await dynamodb.async_query(TABLE_ACCESS_NAME, query_attrs)

    return items


async def get_access_by_url_token(
    url_token: str
) -> List[Dict[str, ProjectType]]:
    """Get user access of a project by the url token"""

    filter_exp = (
        Attr('invitation').exists() &
        Attr('invitation.url_token').eq(url_token)
    )
    scan_attrs = {
        'FilterExpression': filter_exp
    }

    items = await dynamodb.async_scan(TABLE_ACCESS_NAME, scan_attrs)

    return items


async def remove_access(user_email: str, project_name: str) -> bool:
    """Remove project access in dynamo."""
    try:
        delete_attrs = DynamoDeleteType(
            Key={
                'user_email': user_email.lower(),
                'project_name': project_name.lower(),
            }
        )
        resp = await dynamodb.async_delete_item(
            TABLE_ACCESS_NAME, delete_attrs
        )
        return resp
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return False


async def update_access(
    user_email: str,
    project_name: str,
    data: ProjectAccessType
) -> bool:
    """Update project access attributes."""
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {
            'user_email': user_email.lower(),
            'project_name': project_name.lower()
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(
            TABLE_ACCESS_NAME, update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success
