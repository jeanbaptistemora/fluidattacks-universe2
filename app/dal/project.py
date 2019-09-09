"""DAL functions for projects."""

from datetime import datetime

from boto3.dynamodb.conditions import Attr, Key

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


def list_findings(project_name):
    key_exp = Key('project_name').eq(project_name)
    filter_exp = Attr('releaseDate').exists()
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
