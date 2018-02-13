from __future__ import absolute_import
from django.db import connections
from django.utils import timezone
from django.db.utils import OperationalError
from boto3 import resource
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
# pylint: disable=E0402
from __init__ import FI_AWS_DYNAMODB_ACCESS_KEY
from __init__ import FI_AWS_DYNAMODB_SECRET_KEY
import rollbar

def create_user_dao(email, username='-', first_name='-', last_name='-'):
    role = 'None'
    last_login = timezone.now()
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
    if project and description:
        project = project.lower()

        with connections['integrates'].cursor() as cursor:
            query = 'SELECT * FROM projects WHERE project=%s'
            cursor.execute(query, (project,))
            row = cursor.fetchone()

            if row is not None:
                # Project already exists.
                return False

            query = 'INSERT INTO projects(project, description) VALUES (%s, %s)'
            try:
                cursor.execute(query, (project, description,))
                row = cursor.fetchone()
            except OperationalError:
                rollbar.report_exc_info()
                return False
        return True
    return False


def update_user_login_dao(email):
    last_login = timezone.now()

    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET last_login=%s WHERE email = %s'
        cursor.execute(query, (last_login, email,))
        row = cursor.fetchone()
    return row


def get_user_last_login_dao(email):
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT last_login FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return '-'
    return unicode(row[0])


def get_company_dao(email):
    """Obtiene la compania a la que pertenece el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT company FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


def get_role_dao(email):
    """Obtiene el rol que tiene el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT role FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


def get_registered_projects():
    """Obtiene el rol que que tiene el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT DISTINCT(project) FROM projects'
        cursor.execute(query)
        rows = cursor.fetchall()
    if rows is None:
        return "None"
    return rows


def is_registered_dao(email):
    """Verifica si el usuario esta registrado."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT registered FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return '0'
    if row[0] == 1:
        return '1'
    return '0'


def add_access_to_project_dao(email, project_name):
    """Da acceso al proyecto en cuestion."""
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
            query = 'INSERT INTO project_access(user_id, project_id) VALUES(%s, %s)'
            try:
                cursor.execute(query, (user_id[0], project_id[0]))
                return True
            except OperationalError:
                rollbar.report_exc_info()
                return False
    return False


def has_access_to_project_dao(email, project_name):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
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
            query = 'SELECT * FROM project_access WHERE user_id = %s and \
    project_id = %s'
            cursor.execute(query, (user_id[0], project_id[0],))
            has_access = cursor.fetchone()
        else:
            return False

    if has_access is not None:
        return True
    return False

def register(email):
    """Registra usuario en la DB."""
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET registered=1 WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    return row


def assign_role(email, role):
    """Asigna un rol a un usuario en la DB."""
    if role != 'analyst' and role != 'customer':
        return
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET role=%s WHERE email = %s'
        cursor.execute(query, (role, email,))
        row = cursor.fetchone()
    return row


def assign_company(email, company):
    """Asigna una compania a un usuario en la DB."""
    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET company=%s WHERE email = %s'
        cursor.execute(query, (company, email,))
        row = cursor.fetchone()
    return row


def get_project_users(project):
    """Trae los usuarios interesados de un proyecto."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT users.email FROM users LEFT JOIN project_access \
ON users.id = project_access.user_id WHERE project_access.project_id=(SELECT id FROM \
projects where project=%s)'
        try:
            cursor.execute(query, (project,))
            rows = cursor.fetchall()
        except OperationalError:
            rollbar.report_exc_info()
            rows = []
    return rows


def get_projects_by_user(user_id):
    """Trae los usuarios interesados de un proyecto."""
    with connections['integrates'].cursor() as cursor:
        query = "SELECT projects.project, projects.description FROM \
project_access INNER JOIN users ON project_access.user_id=users.id \
INNER JOIN projects ON project_access.project_id=projects.id \
WHERE users.email=%s ORDER BY projects.project ASC"
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
    return rows


def get_findings_amount(project):
    """Actualiza el numero de hallazgos en el proyecto."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT amount FROM findings WHERE project = %s'
        cursor.execute(query, (project,))
        row = cursor.fetchone()
    if row is None:
        return 0
    return row[0]


def update_findings_amount(project, amount):
    """Actualiza el numero de hallazgos en el proyecto."""
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

dynamodb_resource = resource('dynamodb',
                            aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
                            region_name='us-east-1')

def get_comments_dynamo(finding_id):
    """Obtiene los comentarios de un hallazgo"""
    table = dynamodb_resource.Table('comments')
    filter_key = 'finding_id'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        print len(response['Items'])
        if response.get('LastEvaluatedKey'):
            response = table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def create_comment_dynamo(finding_id, email, data):
    """Crea un comentario en un hallazgo"""
    table = dynamodb_resource.Table('comments')
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
            }
            )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def delete_comment_dynamo(finding_id, data):
    """Elimina un comentario en un hallazgo"""
    table = dynamodb_resource.Table('comments')
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
    """Obtiene los comentarios de un hallazgo por el id de un comentario"""
    table = dynamodb_resource.Table('comments')
    filter_key = 'user_id'
    if filter_key and user_id:
        filtering_exp = Key(filter_key).eq(user_id)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def get_remediated_dynamo(finding_id):
    """Obtiene el tratamiento de un hallazgo"""
    table = dynamodb_resource.Table('remediated')
    filter_key = 'finding_id'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        print len(response['Items'])
        if response.get('LastEvaluatedKey'):
            response = table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def add_remediated_dynamo(finding_id, remediated, project, finding_name):
    """Crea o actualiza un registro de remediado"""
    table = dynamodb_resource.Table('remediated')
    item = get_remediated_dynamo(finding_id)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'finding_id': finding_id,
                    'remediated': remediated, 
                    'project': project,
                    'finding_name': finding_name,               
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
    """ Obtiene el tratamiento de todos los hallazgos """
    table = dynamodb_resource.Table('remediated')
    filter_key = 'remediated'
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        print len(response['Items'])
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def get_finding_dynamo(finding_id):
    """Obtiene la informacion de un hallazgo"""
    table = dynamodb_resource.Table('findings')
    filter_key = 'finding_id'
    if filter_key and finding_id:
        filtering_exp = Key(filter_key).eq(finding_id)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def add_finding_dynamo(finding_id, key, value, exist, val):
    """Crea un hallazgo"""
    table = dynamodb_resource.Table('findings')
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
                UpdateExpression='SET ' + key + ' = :val1, ' + exist + '= :val2',
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
    """Elimina un hallazgo"""
    table = dynamodb_resource.Table('findings')
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