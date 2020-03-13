"""DAL functions for projects."""

from datetime import datetime
from typing import Dict, List, Union, cast
import rollbar
from botocore.exceptions import ClientError
import pytz
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings

from backend import util
from backend.dal.event import TABLE as EVENTS_TABLE
from backend.dal.helpers import dynamodb
from backend.typing import (
    Comment as CommentType, Finding as FindingType, Project as ProjectType
)
from backend.dal.finding import (
    get_attributes as get_finding_attributes, get_finding, is_pending_verification,
    TABLE as FINDINGS_TABLE
)
from backend.dal.helpers.analytics import query
from backend.dal.user import get_attributes as get_user_attributes
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')
TABLE_COMMENTS = DYNAMODB_RESOURCE.Table('fi_project_comments')
TABLE_ACCESS = DYNAMODB_RESOURCE.Table('FI_project_access')
TABLE_WEEKLY_REPORT = DYNAMODB_RESOURCE.Table('FI_weekly_report')


def get_current_month_information(project_name: str, query_db: str) -> str:
    """Get information of the current month."""
    project = project_name.lower()
    init_date = datetime.today().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)
    today_date = datetime.today()
    params = (project, init_date, today_date)
    with query() as (curr, conn):
        curr.execute(query_db, params)
        response = curr.fetchone()
        conn.commit()
        if response:
            response = response[0]
        else:
            response = 0
        return response


def get_current_month_authors(project_name: str) -> str:
    """Get the authors of the current month."""
    query_authors = '''SELECT COUNT(DISTINCT(
            Commits.author_name || '_' || Commits.author_email))
            FROM git.commits AS "Commits"
            WHERE (Commits.subscription = %s AND
                (Commits.integration_authored_at BETWEEN %s AND %s));'''
    return get_current_month_information(project_name, query_authors)


def get_current_month_commits(project_name: str) -> str:
    """Get the commits of the current month."""
    query_commits = '''SELECT COUNT(Commits.sha1)
        FROM git.commits AS "Commits"
        WHERE (Commits.subscription = %s AND
            (Commits.authored_at BETWEEN %s AND %s))
        LIMIT 100000;'''
    return get_current_month_information(project_name, query_commits)


def get_active_projects() -> List[str]:
    """Get active project in DynamoDB"""
    filtering_exp = Attr('project_status').eq('ACTIVE') & Attr('project_status').exists()
    projects = get_all(filtering_exp, 'project_name')
    return cast(List[str], [prj['project_name'] for prj in projects])


def get_alive_projects() -> List[str]:
    """Get active and suspended projects in DynamoDB"""
    filtering_exp = Attr('project_status').eq('ACTIVE') | Attr('project_status').eq('SUSPENDED')
    projects = get_all(filtering_exp, 'project_name')
    return cast(List[str], [prj['project_name'] for prj in projects])


def list_drafts(project_name: str) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    filter_exp = Attr('releaseDate').not_exists() \
        | Attr('releaseDate').gt(today)
    response = FINDINGS_TABLE.query(
        FilterExpression=filter_exp,
        IndexName='project_findings',
        KeyConditionExpression=key_exp,
        ProjectionExpression='finding_id')
    drafts = response.get('Items', [])

    while response.get('LastEvaluatedKey'):
        response = FINDINGS_TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            FilterExpression=filter_exp,
            IndexName='project_findings',
            KeyConditionExpression=key_exp,
            ProjectionExpression='finding_id')
        drafts += response.get('Items', [])

    return [draft['finding_id'] for draft in drafts]


def list_findings(project_name: str) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    filter_exp = Attr('releaseDate').exists() & Attr('releaseDate').lte(today)
    response = FINDINGS_TABLE.query(
        FilterExpression=filter_exp,
        IndexName='project_findings',
        KeyConditionExpression=key_exp,
        ProjectionExpression='finding_id')
    findings = response.get('Items', [])

    while response.get('LastEvaluatedKey'):
        response = FINDINGS_TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            FilterExpression=filter_exp,
            IndexName='project_findings',
            KeyConditionExpression=key_exp,
            ProjectionExpression='finding_id')
        findings += response.get('Items', [])

    return [finding['finding_id'] for finding in findings]


def list_events(project_name: str) -> List[str]:
    key_exp = Key('project_name').eq(project_name)
    response = EVENTS_TABLE.query(
        IndexName='project_events',
        KeyConditionExpression=key_exp,
        ProjectionExpression='event_id')
    events = response.get('Items', [])

    while response.get('LastEvaluatedKey'):
        response = EVENTS_TABLE.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            IndexName='project_events',
            KeyConditionExpression=key_exp,
            ProjectionExpression='event_id')
        events += response.get('Items', [])

    return [event['event_id'] for event in events]


def list_internal_managers(project_name: str) -> List[str]:
    all_managers = list_project_managers(project_name)
    internal_managers = \
        [user for user in all_managers if user.endswith('@fluidattacks.com')]
    return internal_managers


def get_all_projects() -> List[str]:
    """Get all projects in DynamoDB"""
    projects = get_all(data_attr='')
    return cast(List[str], [prj['project_name'] for prj in projects])


def get_description(project: str) -> str:
    """ Get the description of a project. """
    description = get_attributes(project, ['description'])
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
    projection_expression = 'user_email, has_access, project_name, responsibility'
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
        users_filtered = [user.get('user_email') for user in users
                          if user.get('has_access', '')]
    else:
        users_filtered = [user.get('user_email') for user in users
                          if not user.get('has_access', '')]
    return users_filtered


def add_all_access_to_project(project: str) -> bool:
    project_exists = exists(project)
    resp = False
    if project_exists:
        users_active = get_users(project, True)
        users_inactive = get_users(project, False)
        all_users = users_active + users_inactive
        users_response = \
            [add_access(user, project, 'has_access', True)
             for user in all_users]
        resp = all(users_response)
    else:
        # project doesn't exists
        pass
    return resp


def remove_all_project_access(project: str) -> bool:
    project_exists = exists(project)
    resp = False
    if project_exists:
        active = True
        users = get_users(project, active)
        users_response = \
            [add_access(user, project, 'has_access', True)
             for user in users]
        resp = all(users_response)
    else:
        # project doesn't exists
        pass
    return resp


def exists(project_name: str) -> bool:
    project = project_name.lower()
    return bool(get_attributes(project, ['project_name']))


def list_project_managers(project_name: str) -> List[str]:
    users_active = get_users(project_name, True)
    users_inactive = get_users(project_name, False)
    all_users = users_active + users_inactive
    managers = \
        [user for user in all_users
         if get_user_attributes(user, ['role']).get('role', '') == 'customeradmin']
    return managers


def get_attributes(
        project_name: str, attributes: List[str] = None) -> Dict[str, Union[str, List[str]]]:
    item_attrs: Dict[str, Union[List[str], Dict[str, str]]] = {
        'Key': {'project_name': project_name},
    }
    if attributes:
        item_attrs['AttributesToGet'] = attributes
    response = TABLE.get_item(**item_attrs)
    return response.get('Item', {})


def get_filtered_list(
        attributes: str = '', filter_expresion: object = None) -> List[Dict[str, ProjectType]]:
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


def is_alive(project: str) -> bool:
    """Validate if a project exist and is not deleted."""
    project_name = project.lower()
    is_valid_project = True
    if exists(project_name):
        project_data = get_attributes(
            project_name.lower(),
            ['deletion_date', 'project_status']
        )
        if project_data.get('project_status') in ['DELETED', 'PENDING_DELETION', 'FINISHED'] or \
           project_data.get('deletion_date'):
            is_valid_project = False
    else:
        is_valid_project = False
    return is_valid_project


def is_request_deletion_user(project: str, user_email: str) -> bool:
    is_user_allowed = False
    if not is_alive(project):
        project_data = get_attributes(
            project.lower(),
            ['historic_deletion', 'project_status']
        )
        historic_deletion = cast(List[Dict[str, str]], project_data.get('historic_deletion'))
        if project_data.get('project_status') == 'PENDING_DELETION':
            is_user_allowed = historic_deletion[-1].get('user') == user_email.lower()
    else:
        is_user_allowed = True
    return is_user_allowed


def update(project_name: str, data: ProjectType) -> bool:
    success = False
    primary_keys = {'project_name': project_name}
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = ['{attr} = :{attr}'.format(attr=attr) for attr in data]
            values = {':{}'.format(attr): data[attr] for attr in data}

            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
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


def remove_user_role(project_name: str, user_email: str, role: str) -> bool:
    """Remove user role in a project."""
    resp = False
    try:
        response = TABLE.update_item(
            Key={
                'project_name': project_name.lower(),
            },
            UpdateExpression='DELETE #rol :val1',
            ExpressionAttributeNames={
                '#rol': role
            },
            ExpressionAttributeValues={
                ':val1': set([user_email])
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def add_comment(project_name: str, email: str, comment_data: CommentType) -> bool:
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


def get_pending_verification_findings(project_name: str) -> List[Dict[str, FindingType]]:
    """Gets findings pending for verification"""
    key_expression = Key('project_name').eq(project_name.lower())
    query_attrs = {
        'IndexName': 'project_findings',
        'KeyConditionExpression': key_expression,
        'ProjectionExpression': 'finding_id'
    }
    response = FINDINGS_TABLE.query(**query_attrs)
    findings = response['Items']
    while response.get('LastEvaluatedKey'):
        response['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = FINDINGS_TABLE.query(**query_attrs)
        findings += response['Items']
    findings = [finding.get('finding_id') for finding in findings]
    pending_to_verify = \
        [finding for finding in findings
         if is_pending_verification(finding)]
    pending_to_verify = \
        [get_finding_attributes(finding, ['finding', 'finding_id', 'project_name'])
         for finding in pending_to_verify]
    return pending_to_verify


def get_released_findings(project_name: str, attrs: str = '') -> List[Dict[str, FindingType]]:
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
    findings = response.get('Items', [])
    while response.get('LastEvaluatedKey'):
        query_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = FINDINGS_TABLE.query(**query_attrs)
        findings += response.get('Items', [])
    findings = [get_finding(finding.get('finding_id')) for finding in findings]
    findings_released = [get_finding(finding.get('finding_id'))
                         for finding in findings if util.validate_release_date(finding)]
    return findings_released


def get_comments(project_name: str) -> List[Dict[str, str]]:
    """ Get comments of a project. """
    key_expression = Key('project_name').eq(project_name)
    response = TABLE_COMMENTS.query(KeyConditionExpression=key_expression)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE_COMMENTS.query(
            KeyConditionExpression=key_expression,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    comment_fullnames = cast(Dict[str, List[str]], {
        mail: list(get_user_attributes(mail, ['last_name', 'first_name']).values())
        for mail in set(item['email'] for item in items)})
    for item in items:
        item['fullname'] = ' '.join(filter(None, comment_fullnames[item['email']][::-1]))
    return items


def add_user(project_name: str, user_email: str, role: str) -> bool:
    """Adding user role in a project."""
    resp = False
    item = get(project_name)
    if item == []:
        try:
            response = TABLE.put_item(
                Item={
                    'project_name': project_name.lower(),
                    role: set([user_email])
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError:
            rollbar.report_exc_info()
    else:
        try:
            response = TABLE.update_item(
                Key={
                    'project_name': project_name.lower(),
                },
                UpdateExpression='ADD #rol :val1',
                ExpressionAttributeNames={
                    '#rol': role
                },
                ExpressionAttributeValues={
                    ':val1': set([user_email])
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError:
            rollbar.report_exc_info()
    return resp


def get(project: str) -> List[ProjectType]:
    """Get a project info."""
    filter_value = project.lower()
    filter_key = 'project_name'
    filtering_exp = Key(filter_key).eq(filter_value)
    response = TABLE.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items


def get_all(filtering_exp: object = '', data_attr: str = '') -> List[ProjectType]:
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


def get_user_access(user_email: str, project_name: str) -> List[Dict[str, ProjectType]]:
    """Get user access of a project."""
    user_email = user_email.lower()
    project_name = project_name.lower()
    filter_key = 'user_email'
    filter_sort = 'project_name'
    filtering_exp = Key(filter_key).eq(user_email) & \
        Key(filter_sort).eq(project_name)
    response = TABLE_ACCESS.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = TABLE_ACCESS.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
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


def weekly_report_dynamo(init_date: str, finish_date: str, registered_users: List[str],
                         logged_users: List[str], companies: List[str]) -> bool:
    """ Save the number of registered and logged users weekly (scheduler used function)."""
    resp = False
    try:
        response = TABLE_WEEKLY_REPORT.put_item(
            Item={
                'init_date': init_date,
                'finish_date': finish_date,
                'registered_users': registered_users,
                'logged_users': logged_users,
                'companies': companies,
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp
