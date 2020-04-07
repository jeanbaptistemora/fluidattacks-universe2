
from datetime import datetime, timedelta

import json
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from graphene import ObjectType, Mutation, List, String, Boolean, Int
from graphql import GraphQLError
from jose import jwt
import rollbar

from backend.decorators import require_login
from backend.domain import project as project_domain, user as user_domain
from backend.entity.project import Project
from backend.exceptions import InvalidExpirationTime

from backend import util
from backend.dal import user as user_dal

from __init__ import FI_GOOGLE_OAUTH2_KEY_ANDROID, FI_GOOGLE_OAUTH2_KEY_IOS


class Me(ObjectType):
    access_token = String()
    authorized = Boolean()
    projects = List(Project)
    remember = Boolean()
    role = String(project_name=String(required=False))

    def __init__(self):
        super(Me, self).__init__()
        self.role = ''
        self.projects = []

    def resolve_role(self, info, project_name=None):
        jwt_content = util.get_jwt_content(info.context)
        user_email = jwt_content['user_email']
        if project_name:
            role = \
                user_domain.get_group_level_role(user_email, project_name)
        else:
            role = \
                user_domain.get_user_level_role(user_email)

        self.role = role

        return self.role

    def resolve_projects(self, info):
        jwt_content = util.get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        for project in user_domain.get_projects(user_email):
            self.projects.append(
                Project(project_name=project,
                        description=project_domain.get_description(project))
            )

        return self.projects

    def resolve_access_token(self, info):
        jwt_content = util.get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        access_token = user_domain.get_data(user_email, 'access_token')
        access_token_dict = {
            'hasAccessToken': bool(access_token),
            'issuedAt': str(access_token.get('iat', '')) if bool(access_token) else ''
        }

        self.access_token = json.dumps(access_token_dict)

        return self.access_token

    def resolve_authorized(self, info):
        """ Resolve user authorization """
        jwt_content = util.get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        self.authorized = user_domain.is_registered(user_email)

        return self.authorized

    def resolve_remember(self, info):
        """ Resolve remember preference """
        jwt_content = util.get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        user_info = user_domain.get_data(user_email, 'legal_remember')
        self.remember = user_info if user_info else False

        return self.remember


class SignIn(Mutation):
    class Arguments():
        auth_token = String(required=True)
        provider = String(required=True)
        push_token = String(required=False)
    authorized = Boolean()
    session_jwt = String()
    success = Boolean()

    @staticmethod
    def mutate(_, info, auth_token, provider, push_token):
        authorized = False
        session_jwt = ''
        success = False

        if provider == 'google':
            try:
                user_info = id_token.verify_oauth2_token(
                    auth_token, requests.Request())

                if user_info['iss'] not in ['accounts.google.com',
                                            'https://accounts.google.com']:
                    rollbar.report_message(
                        'Error: Invalid oauth2 issuer',
                        'error', info.context, user_info['iss'])
                    raise GraphQLError('INVALID_AUTH_TOKEN')
                if user_info['aud'] not in [FI_GOOGLE_OAUTH2_KEY_ANDROID,
                                            FI_GOOGLE_OAUTH2_KEY_IOS]:
                    rollbar.report_message(
                        'Error: Invalid oauth2 audience',
                        'error', info.context, user_info['aud'])
                    raise GraphQLError('INVALID_AUTH_TOKEN')
                email = user_info['email']
                authorized = user_domain.is_registered(email)
                if push_token:
                    user_dal.update(email, {'devices_to_notify': set(push_token)})
                session_jwt = jwt.encode(
                    {
                        'user_email': email,
                        'company': user_domain.get_data(email, 'company'),
                        'first_name': user_info['given_name'],
                        'last_name': user_info['family_name'],
                        'exp': datetime.utcnow() +
                        timedelta(seconds=settings.SESSION_COOKIE_AGE)
                    },
                    algorithm='HS512',
                    key=settings.JWT_SECRET,
                )
                success = True
            except ValueError:
                util.cloudwatch_log(
                    info.context,
                    'Security: Sign in attempt using invalid Google token')
                raise GraphQLError('INVALID_AUTH_TOKEN')
        else:
            rollbar.report_message(
                'Error: Unknown auth provider' + provider, 'error')
            raise GraphQLError('UNKNOWN_AUTH_PROVIDER')

        return SignIn(authorized, session_jwt, success)


class UpdateAccessToken(Mutation):
    class Arguments():
        expiration_time = Int(required=True)
    success = Boolean()
    session_jwt = String()

    @staticmethod
    @require_login
    def mutate(_, info, expiration_time):
        user_info = util.get_jwt_content(info.context)
        email = user_info['user_email']
        token_data = util.calculate_hash_token()
        session_jwt = ''
        success = False

        if util.is_valid_expiration_time(expiration_time):
            session_jwt = jwt.encode(
                {
                    'user_email': email,
                    'company': user_domain.get_data(
                        email, 'company'),
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name'],
                    'jti': token_data['jti'],
                    'iat': datetime.utcnow().timestamp(),
                    'exp': expiration_time
                },
                algorithm='HS512',
                key=settings.JWT_SECRET_API
            )

            success = user_domain.update_access_token(email, token_data)
            if success:
                util.cloudwatch_log(
                    info.context, '{email} update access token'.format(
                        email=user_info['user_email']))
            else:
                util.cloudwatch_log(
                    info.context, '{email} attempted to update access token'
                    .format(email=user_info['user_email']))
        else:
            util.cloudwatch_log(
                info.context, '{email} attempted to use expiration time \
                greater than six months or minor than current time'
                .format(email=user_info['user_email']))
            raise InvalidExpirationTime()

        return UpdateAccessToken(success, session_jwt)


class InvalidateAccessToken(Mutation):
    success = Boolean()

    @staticmethod
    @require_login
    def mutate(_, info):
        user_info = util.get_jwt_content(info.context)

        success = user_domain.remove_access_token(user_info['user_email'])
        if success:
            util.cloudwatch_log(
                info.context, '{email} invalidate access token'.format(
                    email=user_info['user_email']))
        else:
            util.cloudwatch_log(
                info.context, '{email} attempted to invalidate access token'
                .format(email=user_info['user_email']))

        return InvalidateAccessToken(success)


class AcceptLegal(Mutation):
    class Arguments():
        remember = Boolean()
    success = Boolean()

    @staticmethod
    def mutate(_, info, remember):
        user_email = util.get_jwt_content(info.context)['user_email']
        is_registered = user_domain.is_registered(user_email)

        if is_registered:
            user_domain.update_legal_remember(user_email, remember)
            success = True
        else:
            success = False

        return AcceptLegal(success=success)
