from __future__ import absolute_import
from datetime import datetime, timedelta

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from graphene import ObjectType, Mutation, List, String, Boolean
from jose import jwt
import rollbar

from app.decorators import require_login
from app.util import get_jwt_content
from app.services import is_customeradmin
from app.entity.project import Project
from app.dao import integrates_dao
from app import util

from __init__ import FI_GOOGLE_OAUTH2_KEY_APP


class Me(ObjectType):
    role = String(project_name=String(required=False))
    projects = List(Project)

    def __init__(self):
        super(Me, self).__init__()
        self.role = ''
        self.projects = []

    def resolve_role(self, info, project_name=None):
        jwt_content = get_jwt_content(info.context)
        role = jwt_content.get('user_role')
        if project_name and role == 'customer':
            email = jwt_content.get('user_email')
            role = 'customeradmin' if is_customeradmin(
                project_name, email) else 'customer'
        self.role = role

        return self.role

    def resolve_projects(self, info):
        jwt_content = get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        for project in integrates_dao.get_projects_by_user(user_email):
            self.projects.append(
                Project(project_name=project[0], description=project[1])
            )

        return self.projects


class SignIn(Mutation):
    class Arguments(object):
        auth_token = String(required=True)
        provider = String(required=True)
    authorized = Boolean()
    session_jwt = String()
    success = Boolean()

    @staticmethod
    def mutate(_, info, auth_token, provider):
        del info
        authorized = False
        session_jwt = ''
        success = False

        if provider == 'google':
            try:
                user_info = id_token.verify_oauth2_token(
                    auth_token, requests.Request(), FI_GOOGLE_OAUTH2_KEY_APP)

                if user_info['iss'] not in ['accounts.google.com',
                                            'https://accounts.google.com']:
                    raise ValueError("Invalid auth issuer", user_info['iss'])
                else:
                    email = user_info['email']
                    authorized = integrates_dao.is_registered_dao(email) == '1'
                    session_jwt = jwt.encode(
                        {
                            'user_email': email,
                            'user_role': integrates_dao.get_role_dao(email),
                            'exp': datetime.utcnow() +
                            timedelta(seconds=settings.SESSION_COOKIE_AGE)
                        },
                        algorithm='HS512',
                        key=settings.JWT_SECRET,
                    )
                    success = True
            except ValueError:
                util.cloudwatch_log_plain(
                    'Security: Sign in attempt using invalid Google token')
                raise
        else:
            rollbar.report_message(
                'Error: Unknown auth provider' + provider, 'error')
            raise NotImplementedError('Auth provider not supported')

        return SignIn(authorized, session_jwt, success)


class RegisterNotifications(Mutation):
    class Arguments(object):
        push_token = String(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    def mutate(_, info, push_token):
        success = False

        user_data = util.get_jwt_content(info.context)
        email = user_data['user_email']
        success = integrates_dao.add_set_element_dynamo(
            'FI_users', ['email', email], 'devices_to_notify', [push_token])

        return RegisterNotifications(success)
