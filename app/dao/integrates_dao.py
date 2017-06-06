from django.db import connections
from django.utils import timezone


def create_user_dao(email, username='-', first_name='-', last_name='-'):
    role = 'None'
    last_login = timezone.now()
    date_joined = last_login

    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        print (row)
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


def update_user_login_dao(email):
    last_login = timezone.now()

    with connections['integrates'].cursor() as cursor:
        query = 'UPDATE users SET last_login=%s WHERE email = %s'
        cursor.execute(query, (last_login, email,))
        row = cursor.fetchone()
    return row


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
    """Obtiene el rol que que tiene el usuario."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT role FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


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


def has_access_to_project_dao(email, project_name):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        user_id = cursor.fetchone()

        query = 'SELECT * FROM projects WHERE user_id = %s and \
project = %s'
        cursor.execute(query, (user_id, project_name,))
        has_access = cursor.fetchone()
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
    if role != 'admin' and role != 'customer':
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
