"""DAL functions for projects."""

from datetime import datetime

import pytz
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings

from app.dal import integrates_dal, user as user_dal
from app.dal.finding import TABLE as FINDINGS_TABLE
from app.dal.helpers.analytics import query
from app.domain import user as user_domain


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


def list_managers(project_name):
    users_active = get_users(project_name, True)
    users_inactive = get_users(project_name, False)
    all_users = users_active + users_inactive
    managers = \
        [user for user in all_users
         if user_domain.get_data(user, 'role') == 'customeradmin' and
         user.endswith('@fluidattacks.com')]
    return managers


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


def get_users(project, active):
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
    project_exists = integrates_dal.get_project_attributes_dynamo(
        project.lower(), ['project_name'])
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
    project_exists = integrates_dal.get_project_attributes_dynamo(
        project.lower(), ['project_name'])
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
