"""DAL functions for projects."""

from datetime import datetime

import pytz
import rollbar
from boto3.dynamodb.conditions import Attr, Key
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError

from app.dal import integrates_dal
from app.dal.finding import TABLE as FINDINGS_TABLE
from app.dal.helpers.analytics import query


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
    managers = []
    with connections['integrates'].cursor() as cursor:
        try:
            cursor.execute(
                'SELECT users.email FROM users LEFT JOIN project_access '
                'ON users.id = project_access.user_id '
                'WHERE users.role = \'customeradmin\' '
                'AND users.email LIKE \'%%@fluidattacks.com\''
                'AND project_access.project_id=('
                'SELECT id FROM projects WHERE project=%s) ', (project_name, ))
            managers = cursor.fetchall()
        except OperationalError as ex:
            rollbar.report_message(
                'Error: Couldn\'nt list project managers',
                'error', extra_data=ex, payload_data=locals())

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
