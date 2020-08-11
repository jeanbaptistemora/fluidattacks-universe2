"""DAL functions for projects."""

import logging
from datetime import datetime
from typing import (
    cast,
    Dict,
    List,
    NamedTuple,
    Union,
)

import aioboto3
from botocore.exceptions import ClientError
import pytz
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings

from backend import authz, util
from backend.dal.event import TABLE_NAME as EVENTS_TABLE_NAME
from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType,
    DynamoDelete as DynamoDeleteType,
    Finding as FindingType,
    Project as ProjectType
)
from backend.dal.finding import (
    get_finding,
    TABLE_NAME as FINDINGS_TABLE_NAME
)
from backend.dal.user import get_attributes as get_user_attributes
from backend.utils import aio
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
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

    historic_config: list = group_attributes['historic_configuration']

    has_drills: bool = historic_config[-1]['has_drills']
    has_forces: bool = historic_config[-1]['has_forces']
    has_integrates: bool = group_attributes['project_status'] == 'ACTIVE'
    type_: str = historic_config[-1]['type']

    if type_ == 'continuous':

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


async def list_drafts(
        project_name: str,
        table: aioboto3.session.Session.client,
        should_list_deleted: bool = False) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    filter_exp = Attr('releaseDate').not_exists() \
        | Attr('releaseDate').gt(today)
    query_attrs = {
        'KeyConditionExpression': key_exp,
        'FilterExpression': filter_exp,
        'IndexName': 'project_findings',
        'ProjectionExpression': 'finding_id, historic_state'
    }
    response = await table.query(**query_attrs)
    drafts = response.get('Items', [])
    while response.get('LastEvaluatedKey'):
        query_attrs.update(
            {'ExclusiveStartKey': response.get('LastEvaluatedKey')}
        )
        response = await table.query(**query_attrs)
        drafts += response.get('Items', [])

    return [
        draft['finding_id'] for draft in drafts
        if draft.get('historic_state', [{}])[-1].get('state') != 'DELETED'
        or should_list_deleted
    ]


async def list_findings(
        project_name: str,
        table: aioboto3.session.Session.client,
        should_list_deleted: bool = False) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    filter_exp = (
        Attr('releaseDate').exists() &
        Attr('releaseDate').lte(today)
    )
    query_attrs = {
        'KeyConditionExpression': key_exp,
        'FilterExpression': filter_exp,
        'IndexName': 'project_findings',
        'ProjectionExpression': 'finding_id, historic_state'
    }
    response = await table.query(**query_attrs)
    findings = response.get('Items', [])
    while response.get('LastEvaluatedKey'):
        query_attrs.update(
            {'ExclusiveStartKey': response.get('LastEvaluatedKey')}
        )
        response = await table.query(**query_attrs)
        findings += response.get('Items', [])

    return [
        finding['finding_id']
        for finding in findings
        if finding.get(
            'historic_state', [{}]
        )[-1].get('state') != 'DELETED' or
        should_list_deleted
    ]


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
        pre_computed_project_data: dict = None) -> bool:
    project = project_name.lower()
    project_data = (
        pre_computed_project_data or
        await get_attributes(project, ['project_name'])
    )

    return bool(project_data)


async def list_project_managers(group: str) -> List[str]:
    users_active, users_inactive = await aio.materialize([
        get_users(group, True),
        get_users(group, False)
    ])
    all_users = users_active + users_inactive
    users_roles = await aio.materialize([
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
    attributes: List[str] = None,
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
        pre_computed_project_data: dict = None) -> bool:
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


async def can_user_access_pending_deletion(
        project: str,
        role: str,
        should_access_pending: bool = True,
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

    allow_roles = ['admin', 'customeradmin']
    is_user_allowed = False
    if not await is_alive(project, project_data):
        if project_data.get('project_status') == 'PENDING_DELETION':
            is_user_allowed = role in allow_roles and should_access_pending
    else:
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


async def get_released_findings(
        project_name: str,
        attrs: str = '') -> List[Dict[str, FindingType]]:
    """Get all the findings that has been released."""
    key_expression = Key('project_name').eq(project_name.lower())
    filtering_exp = Attr('releaseDate').exists()
    query_attrs = {
        'FilterExpression': filtering_exp,
        'IndexName': 'project_findings',
        'KeyConditionExpression': key_expression
    }
    if attrs and 'releaseDate' not in attrs:
        query_attrs['ProjectionExpression'] = attrs + ', releaseDate'
    if not attrs:
        query_attrs['ProjectionExpression'] = 'finding_id'
    response = await dynamodb.async_query(FINDINGS_TABLE_NAME, query_attrs)

    findings = await aio.materialize([
        get_finding(finding.get('finding_id'))
        for finding in response
    ])
    findings_released = [
        finding
        for finding in findings
        if util.validate_release_date(finding) and
        finding.get(
            'historic_state', [{}]
        )[-1].get('state') != 'DELETED'
    ]
    return findings_released


async def get_comments(project_name: str) -> List[Dict[str, str]]:
    """ Get comments of a project. """
    key_expression = Key('project_name').eq(project_name)
    query_attrs = {
        'KeyConditionExpression': key_expression
    }
    items = await dynamodb.async_query(TABLE_GROUP_COMMENTS, query_attrs)
    comment_name_data = await aio.materialize({
        mail: get_user_attributes(
            mail, ['last_name', 'first_name']
        )
        for mail in set(item['email'] for item in items)
    })
    comment_fullnames = {
        mail: list(fullnames.values())
        for mail, fullnames in comment_name_data.items()
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

    return items


async def get_pending_to_delete() -> List[ProjectType]:
    filtering_exp = Attr('project_status').eq('PENDING_DELETION')
    return await get_all(filtering_exp, 'project_name, historic_deletion')


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
        project_attr: str,
        attr_value: Union[str, bool]) -> bool:
    """Update project access attribute."""
    try:
        set_expression = f'{project_attr} = :{project_attr}'
        expression_values = {f':{project_attr}': attr_value}

        update_attrs = {
            'Key': {
                'user_email': user_email.lower(),
                'project_name': project_name.lower()
            },
            'UpdateExpression': f'SET {set_expression}'.strip(),
            'ExpressionAttributeValues': expression_values
        }
        resp = await dynamodb.async_update_item(
            TABLE_ACCESS_NAME, update_attrs
        )
        return resp
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals))
        return False
