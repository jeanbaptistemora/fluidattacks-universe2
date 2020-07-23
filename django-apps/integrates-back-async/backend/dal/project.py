"""DAL functions for projects."""

from datetime import datetime
from typing import (
    cast,
    Dict,
    List,
    NamedTuple,
    Union,
)
import aioboto3
import rollbar
from asgiref.sync import async_to_sync
from botocore.exceptions import ClientError
import pytz
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings

from backend import authz, util
from backend.dal.event import TABLE as EVENTS_TABLE
from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Project as ProjectType
)
from backend.dal.finding import (
    get_finding,
    TABLE as FINDINGS_TABLE
)
from backend.dal.user import get_attributes as get_user_attributes


DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')
TABLE_COMMENTS = DYNAMODB_RESOURCE.Table('fi_project_comments')
TABLE_ACCESS = DYNAMODB_RESOURCE.Table('FI_project_access')
TABLE_NAME = 'FI_projects'

ServicePolicy = NamedTuple(
    'ServicePolicy',
    [('group', str), ('service', str)]
)


def get_service_policies(group: str) -> List[ServicePolicy]:
    """Return a list of policies for the given group."""
    policies: List[ServicePolicy] = []

    group_attributes: dict = TABLE.get_item(
        AttributesToGet=[
            'historic_configuration',
            'project_status',
        ],
        ConsistentRead=True,
        Key=dict(
            project_name=group.lower(),
        ),
    )

    # There is no such group, let's make an early return
    if 'Item' not in group_attributes:
        return policies

    group_attributes = group_attributes['Item']

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
        rollbar.report_message(
            'Group has invalid type attribute',
            level='critical',
            extra_data=dict(group=group)
        )

    return policies


def get_active_projects() -> List[str]:
    """Get active project in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') &
        Attr('project_status').exists()
    )
    projects = get_all(filtering_exp, 'project_name')
    return cast(
        List[str],
        [prj['project_name'] for prj in projects]
    )


def get_alive_projects() -> List[str]:
    """Get active and suspended projects in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') |
        Attr('project_status').eq('SUSPENDED')
    )
    projects = get_all(filtering_exp, 'project_name')
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


def list_events(project_name: str) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    response = EVENTS_TABLE.query(
        IndexName='project_events',
        KeyConditionExpression=key_exp,
        ProjectionExpression='event_id'
    )
    events = response.get('Items', [])

    while response.get('LastEvaluatedKey'):
        response = EVENTS_TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            IndexName='project_events',
            KeyConditionExpression=key_exp,
            ProjectionExpression='event_id'
        )
        events += response.get('Items', [])

    return [event['event_id'] for event in events]


def list_internal_managers(project_name: str) -> List[str]:
    all_managers = list_project_managers(project_name)
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


def get_users(project: str, active: bool = True) -> List[str]:
    """Get users of a project."""
    project_name = project.lower()
    key_condition = Key('project_name').eq(project_name)
    projection_expression = \
        'user_email, has_access, project_name, responsibility'
    response = TABLE_ACCESS.query(
        IndexName='project_access_users',
        KeyConditionExpression=key_condition,
        ProjectionExpression=projection_expression
    )
    users = response['Items']

    while response.get('LastEvaluatedKey'):
        response = TABLE_ACCESS.query(
            IndexName='project_access_users',
            KeyConditionExpression=key_condition,
            ProjectionExpression=projection_expression,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        users += response['Items']
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


def list_project_managers(group: str) -> List[str]:
    users_active = get_users(group, True)
    users_inactive = get_users(group, False)
    all_users = users_active + users_inactive
    managers = [
        user
        for user in all_users
        if authz.get_group_level_role(user, group) == 'group_manager'
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


def get_filtered_list(
        attributes: str = '', filter_expresion: object = None) -> \
        List[Dict[str, ProjectType]]:
    scan_attrs = {}
    if filter_expresion:
        scan_attrs['FilterExpression'] = filter_expresion
    if attributes:
        scan_attrs['ProjectionExpression'] = attributes
    response = TABLE.scan(**scan_attrs)
    projects = response['Items']

    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = TABLE.scan(**scan_attrs)
        projects += response['Items']
    return projects


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


def update(project_name: str, data: ProjectType) -> bool:
    success = False
    primary_keys = {'project_name': project_name}
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
                f'#{attr} = :{attr}'
                for attr in data
            ]
            names = {
                f'#{attr}': attr
                for attr in data
            }
            values = {
                f':{attr}': data[attr]
                for attr in data
            }

            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='SET ' + ','.join(attributes),
                # By default updates on non-existent items create a new item
                # This condition disables that effect
                ConditionExpression=Attr('project_name').exists(),
                ExpressionAttributeNames=names,
                ExpressionAttributeValues=values,
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_message('Error: Couldn\'nt update project', 'error')
    return success


def create(project: ProjectType) -> bool:
    """Add project to dynamo."""
    resp = False
    try:
        response = TABLE.put_item(Item=project)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def add_comment(project_name: str, email: str, comment_data: CommentType) -> \
        bool:
    """ Add a comment in a project. """
    resp = False
    try:
        payload = {
            'project_name': project_name,
            'email': email
        }
        payload.update(cast(Dict[str, str], comment_data))
        response = TABLE_COMMENTS.put_item(
            Item=payload
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def get_released_findings(project_name: str, attrs: str = '') -> \
        List[Dict[str, FindingType]]:
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
    response = FINDINGS_TABLE.query(**query_attrs)
    items = response.get('Items', [])

    while response.get('LastEvaluatedKey'):
        query_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = FINDINGS_TABLE.query(**query_attrs)
        items += response.get('Items', [])
    findings = [
        async_to_sync(get_finding)(finding.get('finding_id'))
        for finding in items
    ]
    findings_released = [
        finding
        for finding in findings
        if util.validate_release_date(finding) and
        finding.get(
            'historic_state', [{}]
        )[-1].get('state') != 'DELETED'
    ]
    return findings_released


def get_comments(project_name: str) -> List[Dict[str, str]]:
    """ Get comments of a project. """
    key_expression = Key('project_name').eq(project_name)
    response = TABLE_COMMENTS.query(KeyConditionExpression=key_expression)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        response = TABLE_COMMENTS.query(
            KeyConditionExpression=key_expression,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items += response['Items']
    comment_fullnames = cast(
        Dict[str, List[str]],
        {
            mail: list(
                get_user_attributes(
                    mail,
                    ['last_name', 'first_name']
                ).values()
            )
            for mail in set(item['email'] for item in items)
        }
    )
    for item in items:
        item['fullname'] = ' '.join(
            filter(None, comment_fullnames[item['email']][::-1])
        )
    return items


def delete_comment(group_name: str, user_id: str) -> bool:
    resp = False
    try:
        response = TABLE_COMMENTS.delete_item(
            Key={
                'project_name': group_name,
                'user_id': user_id
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message(
            'Error: Couldn\'nt delete group comment',
            'error',
            extra_data=ex
        )
    return resp


def get(project: str) -> ProjectType:
    """Get a project info."""
    filter_value = project.lower()
    filter_key = 'project_name'
    filtering_exp = Key(filter_key).eq(filter_value)
    response = TABLE.query(KeyConditionExpression=filtering_exp)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        response = TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items += response['Items']
    project_info = {}
    if items:
        project_info = items[0]
    return project_info


def get_all(filtering_exp: object = '', data_attr: str = '') -> \
        List[ProjectType]:
    """Get all projects"""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs['FilterExpression'] = filtering_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    response = TABLE.scan(**scan_attrs)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = TABLE.scan(**scan_attrs)
        items += response['Items']

    return items


def get_pending_to_delete() -> List[Dict[str, ProjectType]]:
    filtering_exp = Attr('project_status').eq('PENDING_DELETION')
    return get_filtered_list('project_name, historic_deletion', filtering_exp)


def get_user_access(user_email: str, project_name: str) -> \
        List[Dict[str, ProjectType]]:
    """Get user access of a project."""
    user_email = user_email.lower()
    project_name = project_name.lower()
    filter_key = 'user_email'
    filter_sort = 'project_name'
    filtering_exp = (
        Key(filter_key).eq(user_email) &
        Key(filter_sort).eq(project_name)
    )
    response = TABLE_ACCESS.query(KeyConditionExpression=filtering_exp)
    items = response['Items']

    while True:
        if response.get('LastEvaluatedKey'):
            response = TABLE_ACCESS.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items += response['Items']
        else:
            break
    return items


def add_access(user_email: str, project_name: str,
               project_attr: str, attr_value: Union[str, bool]) -> bool:
    """Add project access attribute."""
    item = get_user_access(user_email, project_name)
    if item == []:
        try:
            response = TABLE_ACCESS.put_item(
                Item={
                    'user_email': user_email.lower(),
                    'project_name': project_name.lower(),
                    project_attr: attr_value
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        return update_access(
            user_email,
            project_name,
            project_attr,
            attr_value
        )


def remove_access(user_email: str, project_name: str) -> bool:
    """Remove project access in dynamo."""
    try:
        response = TABLE_ACCESS.delete_item(
            Key={
                'user_email': user_email.lower(),
                'project_name': project_name.lower(),
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def update_access(user_email: str, project_name: str,
                  project_attr: str, attr_value: Union[str, bool]) -> bool:
    """Update project access attribute."""
    try:
        response = TABLE_ACCESS.update_item(
            Key={
                'user_email': user_email.lower(),
                'project_name': project_name.lower(),
            },
            UpdateExpression='SET #project_attr = :val1',
            ExpressionAttributeNames={
                '#project_attr': project_attr
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False
