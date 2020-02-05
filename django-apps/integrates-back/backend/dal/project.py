"""DAL functions for projects."""

from datetime import datetime
import rollbar
from botocore.exceptions import ClientError
import pytz
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings

from backend.dal import integrates_dal, user as user_dal
from backend.dal.event import TABLE as EVENTS_TABLE
from backend.dal.helpers import dynamodb
from backend.dal.finding import TABLE as FINDINGS_TABLE
from backend.dal.helpers.analytics import query
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
TABLE = DYNAMODB_RESOURCE.Table('FI_projects')
TABLE_COMMENTS = DYNAMODB_RESOURCE.Table('fi_project_comments')


def get_current_month_information(project_name, query_db):
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


def get_current_month_authors(project_name):
    """Get the authors of the current month."""
    query_authors = '''SELECT COUNT(DISTINCT(
            Commits.author_name || '_' || Commits.author_email))
            FROM git.commits AS "Commits"
            WHERE (Commits.subscription = %s AND
                (Commits.integration_authored_at BETWEEN %s AND %s));'''
    return get_current_month_information(project_name, query_authors)


def get_current_month_commits(project_name):
    """Get the commits of the current month."""
    query_commits = '''SELECT COUNT(Commits.sha1)
        FROM git.commits AS "Commits"
        WHERE (Commits.subscription = %s AND
            (Commits.authored_at BETWEEN %s AND %s))
        LIMIT 100000;'''
    return get_current_month_information(project_name, query_commits)


def get_active_projects():
    """Get active project in DynamoDB"""
    filtering_exp = Attr('project_status').eq('ACTIVE') & Attr('project_status').exists()
    projects = integrates_dal.get_projects_data_dynamo(filtering_exp, 'project_name')
    return [prj['project_name'] for prj in projects]


def get_alive_projects():
    """Get active and suspended projects in DynamoDB"""
    filtering_exp = Attr('project_status').eq('ACTIVE') | Attr('project_status').eq('SUSPENDED')
    projects = integrates_dal.get_projects_data_dynamo(filtering_exp, 'project_name')
    return [prj['project_name'] for prj in projects]


def list_drafts(project_name):
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)
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


def list_findings(project_name):
    key_exp = Key('project_name').eq(project_name)
    tzn = pytz.timezone(settings.TIME_ZONE)
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


def list_events(project_name):
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


def list_internal_managers(project_name):
    all_managers = list_project_managers(project_name)
    internal_managers = \
        [user for user in all_managers if user.endswith('@fluidattacks.com')]
    return internal_managers


def get_all_projects():
    """Get all projects in DynamoDB"""
    projects = integrates_dal.get_projects_data_dynamo(data_attr='')
    return [prj['project_name'] for prj in projects]


def get_description(project):
    """ Get the description of a project. """
    description = integrates_dal.get_project_attributes_dynamo(
        project, ['description'])
    project_description = ''
    if description:
        project_description = description.get('description')
    else:
        # project without description
        pass
    return project_description


def get_users(project, active=True):
    """Get users of a project."""
    project_name = project.lower()
    filtering_exp = Key('project_name').eq(project_name)
    users = integrates_dal.get_data_dynamo_filter(
        'FI_project_access', filtering_exp)
    if active:
        users_filtered = [user.get('user_email') for user in users
                          if user.get('has_access', '')]
    else:
        users_filtered = [user.get('user_email') for user in users
                          if not user.get('has_access', '')]
    return users_filtered


def add_all_access_to_project(project):
    project_exists = exists(project)
    resp = False
    if project_exists:
        users_active = get_users(project, True)
        users_inactive = get_users(project, False)
        all_users = users_active + users_inactive
        users_response = \
            [user_dal.update_project_access(user, project, True)
             for user in all_users]
        resp = all(users_response)
    else:
        # project doesn't exists
        pass
    return resp


def remove_all_project_access(project):
    project_exists = exists(project)
    resp = False
    if project_exists:
        active = True
        users = get_users(project, active)
        users_response = \
            [user_dal.update_project_access(user, project, False)
             for user in users]
        resp = all(users_response)
    else:
        # project doesn't exists
        pass
    return resp


def exists(project_name):
    project = project_name.lower()
    return bool(get_attributes(project, ['project_name']))


def list_project_managers(project_name):
    users_active = get_users(project_name, True)
    users_inactive = get_users(project_name, False)
    all_users = users_active + users_inactive
    managers = \
        [user for user in all_users
         if user_dal.get_user_attributes(user, ['role']).get('role', '') == 'customeradmin']
    return managers


def get_attributes(project_name, attributes=None):
    item_attrs = {
        'Key': {'project_name': project_name},
    }
    if attributes:
        item_attrs['AttributesToGet'] = attributes
    response = TABLE.get_item(**item_attrs)
    return response.get('Item', {})


def get_filtered_list(attributes='', filter_expresion=None):
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


def is_alive(project):
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


def is_request_deletion_user(project, user_email):
    is_user_allowed = False
    if not is_alive(project):
        project_data = get_attributes(
            project.lower(),
            ['historic_deletion', 'project_status']
        )
        historic_deletion = project_data.get('historic_deletion', [{}])
        if project_data.get('project_status') == 'PENDING_DELETION':
            is_user_allowed = historic_deletion[-1].get('user') == user_email.lower()
    else:
        is_user_allowed = True
    return is_user_allowed


def update(project_name, data):
    success = False
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key={'project_name': project_name},
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = ['{attr} = :{attr}'.format(attr=attr) for attr in data]
            values = {':{}'.format(attr): data[attr] for attr in data}

            response = TABLE.update_item(
                Key={'project_name': project_name},
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_message('Error: Couldn\'nt update project', 'error')
    return success


def create(project):
    """Add project to dynamo."""
    resp = False
    try:
        response = TABLE.put_item(Item=project)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def add_comment(project_name, email, comment_data):
    """ Add a comment in a project. """
    resp = False
    try:
        payload = {
            'project_name': project_name,
            'email': email
        }
        payload.update(comment_data)
        response = TABLE_COMMENTS.put_item(
            Item=payload
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def get_pending_verification_findings(project_name):
    """Gets findings pending for verification"""
    table = DYNAMODB_RESOURCE.Table('FI_findings')
    filtering_exp = Attr('project_name').eq(project_name.lower()) \
        & Attr('verification_request_date').exists() \
        & Attr('verification_request_date').ne(None)
    response = table.scan(FilterExpression=filtering_exp)
    findings = response['Items']
    while response.get('LastEvaluatedKey'):
        response = table.scan(
            FilterExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        findings += response['Items']

    pending_to_verify = [finding for finding in findings
                         if not finding.get('verification_date')
                         or finding.get('verification_date')
                         < finding.get('verification_request_date')]
    return pending_to_verify


def get_comments(project_name):
    """ Get comments of a project. """
    filter_key = 'project_name'
    filtering_exp = Key(filter_key).eq(project_name)
    response = TABLE_COMMENTS.scan(FilterExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE_COMMENTS.scan(
            FilterExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items


def add_user(project_name, user_email, role):
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


def get(project):
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


def get_pending_projects():
    filtering_exp = Attr('project_status').eq('PENDING_DELETION')
    return get_filtered_list('project_name, historic_deletion', filtering_exp)
