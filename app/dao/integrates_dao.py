from __future__ import absolute_import
from django.db import connections
from django.db.utils import OperationalError
from boto3 import resource
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
# pylint: disable=E0402
from __init__ import FI_AWS_DYNAMODB_ACCESS_KEY
from __init__ import FI_AWS_DYNAMODB_SECRET_KEY
import rollbar
from datetime import datetime


def create_user_dao(email, username='-', first_name='-', last_name='-', first_time='-' ):
    """ Add a new user. """
    role = 'None'
    if first_time == "1":
        last_login = datetime.now()
    else:
        last_login = "1111-1-1 11:11:11"
    date_joined = last_login

    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if row is None:
            query = 'INSERT INTO users(username, first_name, last_name, \
email, role, last_login, date_joined) \
VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query,
                           (username, first_name,
                            last_name, email, role,
                            last_login, date_joined))
            row = cursor.fetchone()
    return row


def create_project_dao(project=None, description=None):
    """ Add a new project. """
    if project and description:
        project = project.lower()

        with connections['integrates'].cursor() as cursor:
            query = 'SELECT * FROM projects WHERE project=%s'
            cursor.execute(query, (project,))
            row = cursor.fetchone()

            if row is not None:
                # Project already exists.
                return False

            query = 'INSERT INTO projects(project, description) \
VALUES (%s, %s)'
            try:
                cursor.execute(query, (project, description,))
                row = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False
        return True
    return False


def update_user_login_dao(email):
    """Update the user's last login date. """
    last_login = datetime.now()

    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET last_login=%s WHERE email = %s'
        cursor.execute(query, (last_login, email,))
        row = cursor.fetchone()
    return row

def update_user_data(email, username, first_name, last_name):
    """Update the user's last login date. """
    date_joined = datetime.now()
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET username=%s, first_name=%s, last_name=%s, date_joined=%s   \
                 WHERE email = %s'
        cursor.execute(query, (username, first_name, last_name, date_joined, email,))
        row = cursor.fetchone()
    return row


def get_user_last_login_dao(email):
    """ Get the user's last login date. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT last_login FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return '-'
    return unicode(row[0])

def get_user_first_login_dao(email):
    """ Get the user's first login date. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT date_joined FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return '-'
    return unicode(row[0])


def get_organization_dao(email):
    """ Get the company of a user. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT company FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


def get_role_dao(email):
    """ Get the role of a user. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT role FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]

def get_project_description(project):
    """ Get the description of a project. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT description FROM projects WHERE project = %s'
        cursor.execute(query, (project,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


def get_registered_projects():
    """ Get all the active projects. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT DISTINCT(project) FROM projects'
        cursor.execute(query)
        rows = cursor.fetchall()
    if rows is None:
        return "None"
    return rows


def is_registered_dao(email):
    """ Check if the user is registered. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT registered FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return '0'
    if row[0] == 1:
        return '1'
    return '0'

def is_in_database(email):
    """ Check if the user exists in DB. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return False
    return True

def has_complete_data(email):
    """ Check if the user has all data in DB . """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT username FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None or row[0] == '-':
        return False
    return True

def add_access_to_project_dao(email, project_name):
    """ Give access of a project to a user. """
    if has_access_to_project_dao(email, project_name):
        return True
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        try:
            cursor.execute(query, (email,))
            user_id = cursor.fetchone()
        except OperationalError:
            user_id = None

        query = 'SELECT id FROM projects WHERE project = %s'
        try:
            cursor.execute(query, (project_name,))
            project_id = cursor.fetchone()
        except OperationalError:
            rollbar.report_exc_info()
            project_id = None

        if project_id and user_id:
            query = 'INSERT INTO project_access(user_id, project_id, \
has_access) VALUES(%s, %s, %s)'
            try:
                cursor.execute(query, (user_id[0], project_id[0], 1))
                return True
            except OperationalError:
                rollbar.report_exc_info()
                return False
    return False


def has_access_to_project_dao(email, project_name):
    """ Verify that a user has access to a specific project. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        try:
            cursor.execute(query, (email,))
            user_id = cursor.fetchone()
        except OperationalError:
            rollbar.report_exc_info()
            return False

        query = 'SELECT id FROM projects WHERE project = %s'
        try:
            cursor.execute(query, (project_name.lower(),))
            project_id = cursor.fetchone()
        except OperationalError:
            rollbar.report_exc_info()
            return False

        if project_id and user_id:
            query = 'SELECT has_access FROM project_access \
WHERE user_id = %s and project_id = %s'
            cursor.execute(query, (user_id[0], project_id[0],))
            has_access = cursor.fetchone()
        else:
            return False
    if has_access is not None:
        if has_access[0] == 1:
            return True
    return False


def remove_all_access_to_project_dao(project_name=None):
    """ Remove access permission to all users in a project. """
    if project_name:
        project_name = project_name.lower()

        with connections['integrates'].cursor() as cursor:
            query = 'SELECT id FROM projects WHERE project = %s'
            try:
                cursor.execute(query, (project_name,))
                project_id = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False

            if project_id:
                query = 'UPDATE project_access SET has_access=0 \
WHERE project_id = %s'
                try:
                    cursor.execute(query, (project_id[0],))
                    cursor.fetchone()
                    return True
                except OperationalError:
                    rollbar.report_exc_info()
                    return False
            else:
                return False
    return False


def add_all_access_to_project_dao(project_name=None):
    """ Add access permission to all users of a project. """
    if project_name:
        project_name = project_name.lower()

        with connections['integrates'].cursor() as cursor:
            query = 'SELECT id FROM projects WHERE project = %s'
            try:
                cursor.execute(query, (project_name,))
                project_id = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False

            if project_id:
                query = 'UPDATE project_access SET has_access=1 \
WHERE project_id = %s'
                try:
                    cursor.execute(query, (project_id[0],))
                    cursor.fetchone()
                    return True
                except OperationalError:
                    rollbar.report_exc_info()
                    return False
            else:
                return False
    return False


def register(email):
    """ Register user in the DB. """
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET registered=1 WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    return row


def assign_role(email, role):
    """ Assigns a role to a user in the DB. """
    if (role != 'analyst' and role != 'customer' and
            role != 'admin' and role != 'customeradmin'):
        return False
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET role=%s WHERE email = %s'
        cursor.execute(query, (role, email,))
        row = cursor.fetchone()
    return row

def assign_admin_role(email):
    """ Assigns admin role to a costumer in the DB. """
    role = get_role_dao(email)
    if role != 'customer':
        return False
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET role=%s WHERE email = %s'
        cursor.execute(query, ('customeradmin', email,))
    return True


def assign_company(email, company):
    """ Assigns a company to a user in the DB."""
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET company=%s WHERE email = %s'
        cursor.execute(query, (company, email,))
        row = cursor.fetchone()
    return row


def get_project_users(project):
    """ Gets the users related to a project. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT users.email, project_access.has_access \
FROM users LEFT JOIN project_access ON users.id = project_access.user_id \
WHERE project_access.project_id=(SELECT id FROM projects where project=%s)'
        try:
            cursor.execute(query, (project,))
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows


def get_projects_by_user(user_id):
    """ Gets the users related to a project. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT projects.project, projects.description, \
project_access.has_access FROM project_access INNER JOIN users \
ON project_access.user_id=users.id INNER JOIN projects \
ON project_access.project_id=projects.id WHERE users.email=%s \
ORDER BY projects.project ASC'
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
    return rows


def get_findings_amount(project):
    """ Gets the amount of findings in a project. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT amount FROM findings WHERE project = %s'
        cursor.execute(query, (project,))
        row = cursor.fetchone()
    if row is None:
        return 0
    return row[0]


def get_vulns_by_project_dynamo(project_name):
    """ Gets findings info by project name. """
    table = dynamodb_resource.Table('FI_findings_email')
    filter_key = 'project_name'
    if filter_key and project_name:
        filtering_exp = Key(filter_key).eq(project_name)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def get_user_dynamo(email):
    """ Get legal notice acceptance status """
    table = dynamodb_resource.Table('FI_users')
    filter_key = 'email'
    if filter_key and email:
        response = table.query(KeyConditionExpression=Key(filter_key).eq(email))
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def update_legal_remember_dynamo(email, remember):
    """ Remember legal notice acceptance """
    table = dynamodb_resource.Table('FI_users')
    item = get_user_dynamo(email)
    if item == []:
        print "item empty"
        try:
            response = table.put_item(
                Item={
                    'email': email,
                    'legal_remember': remember
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression='SET legal_remember = :val1',
                ExpressionAttributeValues={
                    ':val1': remember
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False

def add_phone_to_user_dynamo(email, phone):
    """Update user phone number."""
    table = dynamodb_resource.Table('FI_users')
    item = get_user_dynamo(email)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'email': email,
                    'phone': phone
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression='SET phone = :val1',
                ExpressionAttributeValues={
                    ':val1': phone
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False

def get_vulns_by_id_dynamo(project_name, unique_id):
    """ Gets findings info by finding ID. """
    table = dynamodb_resource.Table('FI_findings_email')
    filter_key = 'project_name'
    filter_sort = 'unique_id'
    if filter_key and project_name and filter_sort and unique_id:
        response = table.query(KeyConditionExpression=Key(filter_key).
                               eq(project_name) & Key(filter_sort).
                               eq(unique_id))
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_or_update_vulns_dynamo(project_name, unique_id, vuln_hoy):
    """ Create or update a vulnerability. """
    table = dynamodb_resource.Table('FI_findings_email')
    item = get_vulns_by_id_dynamo(project_name, unique_id)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'project_name': project_name,
                    'unique_id': int(unique_id),
                    'vuln_hoy': int(vuln_hoy),
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'project_name': project_name,
                    'unique_id': int(unique_id),
                },
                UpdateExpression='SET vuln_hoy = :val1',
                ExpressionAttributeValues={
                    ':val1': int(vuln_hoy)
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def get_company_alert_dynamo(company_name, project_name):
    """ Get alerts of a company. """
    company_name = company_name.lower()
    project_name = project_name.lower()
    table = dynamodb_resource.Table('FI_alerts_by_company')
    filter_key = 'company_name'
    filter_sort = 'project_name'
    if project_name == 'all':
        if filter_key and company_name:
            response = table.query(
                KeyConditionExpression=Key(filter_key).eq(company_name))
        else:
            response = table.query()
    else:
        if filter_key and company_name and filter_sort and project_name:
            response = table.query(KeyConditionExpression=Key(filter_key).
                                   eq(company_name) & Key(filter_sort).
                                   eq(project_name))
        else:
            response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def set_company_alert_dynamo(message, company_name, project_name):
    """ Create, update or activate an alert for a company. """
    project = project_name.lower()
    if project != 'all':
        with connections['integrates'].cursor() as cursor:
            query = 'SELECT * FROM projects WHERE project=%s'
            cursor.execute(query, (project,))
            row = cursor.fetchone()
            if row is None:
                # Project already exists.
                return False
    company_name = company_name.lower()
    project_name = project_name.lower()
    table = dynamodb_resource.Table('FI_alerts_by_company')
    item = get_company_alert_dynamo(company_name, project_name)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'company_name': company_name,
                    'project_name': project_name,
                    'message': message,
                    'status_act': '1',
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        for a in item:
            try:
                response = table.update_item(
                    Key={
                        'company_name': a['company_name'],
                        'project_name': a['project_name'],
                    },
                    UpdateExpression='SET message = :val1, status_act = :val2',
                    ExpressionAttributeValues={
                        ':val1': str(message),
                        ':val2': '1',
                    }
                )
            except ClientError:
                rollbar.report_exc_info()
                return False
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp


def change_status_company_alert_dynamo(message, company_name, project_name):
    """ Activate or deactivate the alert of a company. """
    message = message.lower()
    company_name = company_name.lower()
    project_name = project_name.lower()
    table = dynamodb_resource.Table('FI_alerts_by_company')
    if ((project_name == 'all' and message == 'deactivate') or
            (project_name != 'all' and message == 'deactivate')):
        status = '0'
    else:
        status = '1'
    item = get_company_alert_dynamo(company_name, project_name)
    for a in item:
        payload = {'company_name': a['company_name'],
                   'project_name': a['project_name'], }
        try:
            table.update_item(
                Key=payload,
                UpdateExpression='SET status_act = :val1',
                ExpressionAttributeValues={
                    ':val1': status,
                }
            )
        except ClientError:
            rollbar.report_exc_info()
            return False


def update_findings_amount(project, amount):
    """ Update amount of findings in a project."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT * FROM findings WHERE project = %s'
        cursor.execute(query, (project,))
        row = cursor.fetchone()
        if row is None:
            query = 'INSERT INTO findings(project, amount) VALUES(%s, %s)'
            cursor.execute(query, (project, amount,))
            row = cursor.fetchone()
        else:
            query = 'UPDATE findings SET amount=%s WHERE project = %s'
            cursor.execute(query, (amount, project,))
            row = cursor.fetchone()
    return row


def remove_access_project_dao(email=None, project_name=None):
    """ Remove a user's access to a project. """
    if email and project_name:
        project_name = project_name.lower()

        with connections['integrates'].cursor() as cursor:
            query = 'SELECT id FROM users WHERE email = %s'
            try:
                cursor.execute(query, (email,))
                user_id = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False

            query = 'SELECT id FROM projects WHERE project = %s'
            try:
                cursor.execute(query, (project_name,))
                project_id = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False

            if project_id and user_id:
                query = 'DELETE FROM project_access WHERE user_id = %s and \
        project_id = %s'
                try:
                    cursor.execute(query, (user_id[0], project_id[0],))
                    cursor.fetchone()
                    return True
                except OperationalError:
                    rollbar.report_exc_info()
                    return False
            else:
                return False
    return False


def all_users_report(company_name, finish_date):
    """ Gets the number of registered users in integrates. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT COUNT(id) FROM users WHERE company != %s and \
        registered = 1 and date_joined <= %s'
        try:
            cursor.execute(query, (company_name, finish_date,))
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows


def logging_users_report(company_name, init_date, finish_date):
    """ Gets the number of logged in users in integrates. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT COUNT(id) FROM users WHERE company != %s and \
        registered = 1 and last_login >= %s and last_login <= %s'
        try:
            cursor.execute(query, (company_name, init_date, finish_date,))
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows


def all_inactive_users():
    """ Gets amount of inactive users in Integrates. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id, last_login FROM users WHERE registered = 0'
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows


def delete_user(user_id=None):
    """ Delete user of Integrates DB. """
    if user_id:
        with connections['integrates'].cursor() as cursor:
            query = 'DELETE FROM users WHERE id = %s'
            try:
                cursor.execute(query, (user_id,))
                cursor.fetchone()
                return True
            except OperationalError:
                rollbar.report_exc_info()
                return False
        return False

def get_admins():
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT email FROM users WHERE role = %s'
        try:
            cursor.execute(query, ("admin", ))
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows

dynamodb_resource = resource('dynamodb',
                             aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
                             aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
                             region_name='us-east-1')


def get_comments_dynamo(finding_id, comment_type):
    """ Get comments of a finding. """
    table = dynamodb_resource.Table('FI_comments')
    filter_key = 'finding_id'
    filter_attribute = 'comment_type'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id) & Key(filter_attribute).eq(comment_type)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def create_comment_dynamo(finding_id, email, data):
    """ Create a comment in a finding. """
    table = dynamodb_resource.Table('FI_comments')
    try:
        response = table.put_item(
            Item={
                'finding_id': finding_id,
                'user_id': int(data["data[id]"]),
                'content': data["data[content]"],
                'created': data["data[created]"],
                'email': email,
                'fullname': data["data[fullname]"],
                'modified': data["data[modified]"],
                'parent': data["data[parent]"],
                'comment_type': data["data[commentType]"]
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def delete_comment_dynamo(finding_id, data):
    """ Delete a comment in a finding. """
    table = dynamodb_resource.Table('FI_comments')
    try:
        response = table.delete_item(
            Key={
                'finding_id': finding_id,
                'user_id': int(data["data[id]"])
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_replayer_dynamo(user_id):
    """ Gets comments by the ID parent comment. """
    table = dynamodb_resource.Table('FI_comments')
    filter_key = 'user_id'
    if filter_key and user_id:
        filtering_exp = Key(filter_key).eq(user_id)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def get_remediated_dynamo(finding_id):
    """ Gets the remediated status of a finding. """
    table = dynamodb_resource.Table('FI_remediated')
    filter_key = 'finding_id'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_remediated_dynamo(finding_id, remediated, project, finding_name):
    """Create or update a remediate status."""
    table = dynamodb_resource.Table('FI_remediated')
    item = get_remediated_dynamo(finding_id)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'finding_id': finding_id,
                    'remediated': remediated,
                    'project': project.lower(),
                    'finding_name': finding_name
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'finding_id': finding_id,
                },
                UpdateExpression='SET remediated = :val1',
                ExpressionAttributeValues={
                    ':val1': remediated
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def get_remediated_allfindings_dynamo(filter_value):
    """ Gets the treatment of all the findings. """
    table = dynamodb_resource.Table('FI_remediated')
    filter_key = 'remediated'
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def get_project_dynamo(project):
    """Get a project info."""
    filter_value = project.lower()
    table = dynamodb_resource.Table('FI_projects')
    filter_key = 'project_name'
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_project_dynamo(project, description, companies):
    """Add project to dynamo."""
    table = dynamodb_resource.Table('FI_projects')
    try:
        response = table.put_item(
            Item={
                'project_name': project.lower(),
                'description': description,
                'companies': companies
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def add_release_toproject_dynamo(project_name, release_val, last_release):
    """Add or Update release status in a project."""
    table = dynamodb_resource.Table('FI_projects')
    item = get_project_dynamo(project_name)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'project_name': project_name.lower(),
                    'hasRelease': release_val,
                    'lastRelease': last_release
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'project_name': project_name.lower(),
                },
                UpdateExpression='SET hasRelease = :val1, lastRelease = :val2',
                ExpressionAttributeValues={
                    ':val1': release_val,
                    ':val2': last_release
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def add_user_to_project_dynamo(project_name, user_email, role):
    """Adding user role in a project."""
    table = dynamodb_resource.Table('FI_projects')
    item = get_project_dynamo(project_name)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'project_name': project_name.lower(),
                    role: set([user_email])
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
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
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def remove_role_to_project_dynamo(project_name, user_email, role):
    """Remove user role in a project."""
    table = dynamodb_resource.Table('FI_projects')
    try:
        response = table.update_item(
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
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_finding_dynamo(finding_id):
    """Gets the info of a finding."""
    table = dynamodb_resource.Table('FI_findings')
    filter_key = 'finding_id'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_finding_dynamo(finding_id, key, value, exist, val):
    """ Create a finding in DynamoDB. """
    table = dynamodb_resource.Table('FI_findings')
    item = get_finding_dynamo(finding_id)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'finding_id': finding_id,
                    key: value,
                    exist: val
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'finding_id': finding_id,
                },
                UpdateExpression='SET ' + key + '= :val1,' + exist + '= :val2',
                ExpressionAttributeValues={
                    ':val1': value,
                    ':val2': val
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def delete_finding_dynamo(finding_id):
    """ Delete a finding in DynamoDb."""
    table = dynamodb_resource.Table('FI_findings')
    try:
        response = table.delete_item(
            Key={
                'finding_id': finding_id,
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_toe_dynamo(project):
    """ Gets TOE of a proyect. """
    table = dynamodb_resource.Table('FI_toe')
    filter_key = 'project'
    if filter_key and project:
        filtering_exp = Key(filter_key).eq(project)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def weekly_report_dynamo(
        init_date, finish_date, registered_users, logged_users):
    """ Save the number of registered and logged users weekly. """
    table = dynamodb_resource.Table('FI_weekly_report')
    try:
        response = table.put_item(
            Item={
                'init_date': init_date,
                'finish_date': finish_date,
                'registered_users': registered_users,
                'logged_users': logged_users,
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False

def get_continuous_info():
    """ Gets info of all continuous projects. """
    table = dynamodb_resource.Table('FI_toe')
    filter_key = 'last_update'
    if filter_key:
        filtering_exp = Key(filter_key).eq(str(datetime.now().date()))
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def update_company_dynamo(project_name, companies):
    """ Update a company to a project. """
    table = dynamodb_resource.Table('FI_projects')
    item = get_project_dynamo(project_name)
    if item == [] or 'companies' not in item[0]:
        return False
    else:
        try:
            response = table.update_item(
                Key={
                    'project_name': project_name.lower(),
                },
                UpdateExpression='SET companies = list_append(companies, :val1)',
                ExpressionAttributeValues={
                    ':val1': companies
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def get_project_access_dynamo(user_email, project_name):
    """Get user access of a project."""
    user_email = user_email.lower()
    project_name = project_name.lower()
    table = dynamodb_resource.Table('FI_project_access')
    filter_key = 'user_email'
    filter_sort = 'project_name'
    if user_email and project_name:
        response = table.query(KeyConditionExpression=Key(filter_key).
                               eq(user_email) & Key(filter_sort).
                               eq(project_name))
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_project_access_dynamo(
        user_email, project_name, project_attr, attr_value):
    """Add project access attribute."""
    table = dynamodb_resource.Table('FI_project_access')
    item = get_project_access_dynamo(user_email, project_name)
    if item == []:
        try:
            response = table.put_item(
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
        return update_project_access_dynamo(
            user_email,
            project_name,
            project_attr,
            attr_value
        )


def update_project_access_dynamo(
        user_email, project_name, project_attr, attr_value):
    """Update project access attribute."""
    table = dynamodb_resource.Table('FI_project_access')
    try:
        response = table.update_item(
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


def add_repository_dynamo(project_name, data, attr_name):
    """Add repository information to projects table."""
    table = dynamodb_resource.Table('FI_projects')
    item = get_project_dynamo(project_name)
    if not item:
        try:
            response = table.put_item(
                Item={
                    'project_name': project_name.lower(),
                    attr_name: data,
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        return update_repository_dynamo(
            project_name,
            data, attr_name,
            item
        )


def update_repository_dynamo(project_name, data, attr_name, item):
    """Update repository information to projects table."""
    table = dynamodb_resource.Table('FI_projects')
    try:
        if attr_name not in item[0]:
            table.update_item(
                Key={
                    'project_name': project_name.lower(),
                },
                UpdateExpression='SET #attrName = :val1',
                ExpressionAttributeNames={
                    '#attrName': attr_name
                },
                ExpressionAttributeValues={
                    ':val1': []
                }
            )
        update_response = table.update_item(
            Key={
                'project_name': project_name.lower(),
            },
            UpdateExpression='SET #attrName = list_append(#attrName, :val1)',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': data
            }
        )
        resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def remove_repository_dynamo(project_name, attr_name, index):
    """Update repository information to projects table."""
    table = dynamodb_resource.Table('FI_projects')
    try:
        response = table.update_item(
            Key={
                'project_name': project_name.lower(),
            },
            UpdateExpression='REMOVE #attrName[' + str(index) + ']',
            ExpressionAttributeNames={
                '#attrName': attr_name
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False
