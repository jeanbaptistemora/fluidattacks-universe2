from django.db import connections
from django.utils import timezone
from django.db.utils import OperationalError


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
            project_id = None

        if project_id and user_id:
            query = 'INSERT INTO project_access(user_id, project_id) VALUES(%s, %s)'
            try:
                cursor.execute(query, (user_id[0], project_id[0]))
                success = True
            except OperationalError:
                success = False
        else:
            success = False
    return success


def has_access_to_project_dao(email, project_name):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT id FROM users WHERE email = %s'
        try:
            cursor.execute(query, (email,))
            user_id = cursor.fetchone()
        except OperationalError:
            return False

        query = 'SELECT id FROM projects WHERE project = %s'
        try:
            cursor.execute(query, (project_name.lower(),))
            project_id = cursor.fetchone()
        except OperationalError:
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
        cursor.execute(query, (project,))
        rows = cursor.fetchall()
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
