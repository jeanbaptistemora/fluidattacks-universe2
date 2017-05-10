from django.db import connections
from django.db import models
from django.utils import timezone


def create_user_dao(username, first_name, last_name, email):
    role = 'customer'
    last_login = timezone.now()
    date_joined = last_login

    with connections['integrates'].cursor() as cursor:
        query = 'INSERT INTO users(username, first_name, last_name, \
email, role, last_login, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query,
                       (username, first_name,
                        last_name, email, role,
                        last_login, date_joined))
        row = cursor.fetchone()
    return row


def update_user_login_dao(email):
    last_login = timezone.now()

    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET last_login="%s" WHERE email = "%s"'
        cursor.execute(query, (last_login, email,))
        row = cursor.fetchone()
    return row


def get_company_dao(email):
    """Obtiene la compania a la que pertenece el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT company FROM users WHERE email = "%s"'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    return row


def get_role_dao(email):
    """Obtiene el rol que que tiene el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT role FROM users WHERE email = "%s"'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    return row


def is_registered_dao(email):
    """Verifica si el usuario esta registrado."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT registered FROM users WHERE email = "%s"'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    return row


def has_access_to_project_dao(email, project_name):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = "%s"'
        cursor.execute(query, (email,))
        user_id = cursor.fetchone()

        query = 'SELECT * FROM projects WHERE id = "%s" and \
project = "%s"'
        cursor.execute(query, (email, project_name,))
        has_access = cursor.fetchone()
    return has_access
