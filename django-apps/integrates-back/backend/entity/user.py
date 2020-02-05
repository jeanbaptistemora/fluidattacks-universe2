# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=too-many-instance-attributes
# Disabling this rule is necessary to have more than 7 instance attributes

import threading
import re
from datetime import datetime

import rollbar
from graphene import ObjectType, Mutation, String, Boolean, Field, List
from graphql.error import GraphQLError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from backend.decorators import (
    require_login, require_project_access, new_require_role
)
from backend.domain import project as project_domain, user as user_domain
from backend.services import (
    get_user_role, is_customeradmin, has_responsibility, has_phone_number,
    has_access_to_project
)
from backend.exceptions import UserNotFound
from backend.mailer import send_mail_access_granted

from backend import util
from backend.dal import integrates_dal


class User(ObjectType):
    """ GraphQL Entity for Project Users """
    email = String()
    role = String()
    responsibility = String()
    phone_number = String()
    organization = String()
    first_login = String()
    last_login = String()
    list_projects = List(String)

    def __init__(self, project_name, user_email, role=None):
        self.email = user_email
        self.role = ''
        self.responsibility = ''
        self.phone_number = ''
        self.organization = ''
        self.first_login = '-'
        self.last_login = [-1, -1]
        if not project_name:
            projs_active = \
                ['{proj}: {description} - Active'.format(
                    proj=proj,
                    description=project_domain.get_description(proj))
                    for proj in user_domain.get_projects(self.email)]
            projs_suspended = \
                ['{proj}: {description} - Suspended'.format(
                    proj=proj,
                    description=project_domain.get_description(proj))
                    for proj in user_domain.get_projects(
                        self.email, active=False)]
            self.list_projects = projs_active + projs_suspended
        else:
            self.list_projects = []

        last_login = user_domain.get_data(user_email, 'last_login')

        if last_login == '1111-1-1 11:11:11' or not last_login:
            self.last_login = [-1, -1]
        else:
            dates_difference = \
                datetime.now() - datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
            diff_last_login = [dates_difference.days, dates_difference.seconds]
            self.last_login = diff_last_login

        self.first_login = user_domain.get_data(user_email, 'date_joined')
        organization = user_domain.get_data(user_email, 'company')
        self.organization = organization.title()
        self.responsibility = has_responsibility(
            project_name, user_email) if project_name else ''
        self.phone_number = has_phone_number(user_email)
        user_role = user_domain.get_data(user_email, 'role')

        if project_name and is_customeradmin(project_name, user_email):
            self.role = 'customer_admin'
        elif user_role == 'customeradmin':
            self.role = 'customer'
        else:
            self.role = user_role

        if project_name and role:
            if role == 'admin':
                has_access = has_access_to_project(
                    user_email, project_name, self.role)
            else:
                has_access = user_domain.get_project_access(
                    user_email, project_name)

            if not user_domain.get_data(user_email, 'email') or \
               not has_access:
                raise UserNotFound()

    def resolve_email(self, info):
        """ Resolve user email """
        del info
        return self.email.lower()

    def resolve_role(self, info):
        """ Resolve user role """
        del info
        return self.role

    def resolve_responsibility(self, info):
        """ Resolve user responsibility in the given project """
        del info
        return self.responsibility

    def resolve_phone_number(self, info):
        """ Resolve user phone number """
        del info
        return self.phone_number

    def resolve_organization(self, info):
        """ Resolve user organization """
        del info
        return self.organization

    def resolve_first_login(self, info):
        """ Resolve user's first login date """
        del info
        return self.first_login

    def resolve_last_login(self, info):
        """ Resolve user's last login date """
        del info
        return self.last_login

    @new_require_role
    def resolve_list_projects(self, info):
        del info
        return self.list_projects


class GrantUserAccess(Mutation):
    """Grant access to a given project."""

    class Arguments():
        project_name = String()
        email = String(required=True)
        organization = String(required=True)
        responsibility = String()
        role = String(required=True)
        phone_number = String()

    granted_user = Field(User)
    success = Boolean()

    @require_login
    @new_require_role
    @require_project_access
    def mutate(self, info, **query_args):
        project_name = query_args.get('project_name')
        success = False
        user_data = util.get_jwt_content(info.context)
        role = get_user_role(user_data)
        new_user_data = {
            'email': query_args.get('email'),
            'organization': query_args.get('organization'),
            'responsibility': query_args.get('responsibility', '-'),
            'role': query_args.get('role'),
            'phone_number': query_args.get('phone_number')
        }

        if (role == 'admin'
                and new_user_data['role'] in ['admin', 'analyst', 'customer', 'customeradmin']) \
            or (is_customeradmin(project_name, user_data['user_email'])
                and new_user_data['role'] in ['customer', 'customeradmin']):
            if create_new_user(info.context, new_user_data,
                               project_name):
                success = True
            else:
                rollbar.report_message('Error: Couldn\'t grant access to project',
                                       'error', info.context)
        else:
            rollbar.report_message('Error: Invalid role provided: ' +
                                   new_user_data['role'], 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.invalidate_cache(query_args.get('email'))
            util.cloudwatch_log(info.context, 'Security: Given grant access to {user} \
                in {project} project'.format(user=query_args.get('email'), project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to give grant \
                access to {user} in {project} project'.format(user=query_args.get('email'),
                                                              project=project_name))
        ret = \
            GrantUserAccess(success=success,
                            granted_user=User(project_name,
                                              new_user_data['email']))
        return ret


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise GraphQLError('Exception - Email is not valid')


def validate_field(field):
    if field[0].isalnum() or (field[0] == "-" or field[0] is None):
        return True
    raise GraphQLError('Exception - Parameter is not valid')


def validate_phone_field(phone_field):
    if re.match((r'(^\+\d+$)|(^\d+$)|(^$)|(^-$)'), phone_field):
        return True
    raise GraphQLError('Exception - Parameter is not valid')


def create_new_user(context, new_user_data, project_name):
    analizable_list = list(new_user_data.values())[1:-1]
    if (
        all(validate_field(field) for field in analizable_list) and
        validate_phone_field(new_user_data['phone_number']) and
        validate_email_address(new_user_data['email'])
    ):
        email = new_user_data['email']
        organization = new_user_data['organization']
        responsibility = new_user_data['responsibility']
        role = new_user_data['role']
        phone_number = new_user_data['phone_number']
        primary_keys_dynamo = ['email', email.lower()]
    else:
        return False

    success = False

    if not user_domain.get_data(email, 'email'):
        integrates_dal.add_multiple_attributes_dynamo(
            'FI_users', primary_keys_dynamo, {'company': organization.lower(),
                                              'phone': phone_number})
    if not user_domain.is_registered(email):
        user_domain.register(email)
        user_domain.assign_role(email, role)
        user_domain.update_user_attribute(
            email, organization.lower(), 'company')
    elif user_domain.is_registered(email):
        user_domain.assign_role(email, role)
    if project_name and responsibility and len(responsibility) <= 50:
        integrates_dal.add_project_access_dynamo(email, project_name,
                                                 'responsibility',
                                                 responsibility)
    else:
        util.cloudwatch_log(
            context,
            'Security: {email} Attempted to add responsibility to project \
                {project} without validation'.format(email=email,
                                                     project=project_name)
        )
    if phone_number and phone_number[1:].isdigit():
        user_domain.add_phone_to_user(email, phone_number)
    if project_name and role == 'customeradmin':
        project_domain.add_user(project_name.lower(), email.lower(), role)
    if project_name and user_domain.update_project_access(email, project_name, True):
        description = project_domain.get_description(project_name.lower())
        project_url = \
            'https://fluidattacks.com/integrates/dashboard#!/project/' \
            + project_name.lower() + '/indicators'
        mail_to = [email]
        context = {
            'admin': email,
            'project': project_name,
            'project_description': description,
            'project_url': project_url,
        }
        email_send_thread = \
            threading.Thread(name='Access granted email thread',
                             target=send_mail_access_granted,
                             args=(mail_to, context,))
        email_send_thread.start()
        success = True
    if not project_name:
        mail_to = [email]
        context = {
            'admin': email,
        }
        email_send_thread = \
            threading.Thread(name='Access granted email thread',
                             target=send_mail_access_granted,
                             args=(mail_to, context,))
        email_send_thread.start()
        success = True
    return success


class RemoveUserAccess(Mutation):
    """Remove user of a given project."""

    class Arguments():
        project_name = String()
        user_email = String()

    removed_email = String()
    success = Boolean()

    @require_login
    @new_require_role
    @require_project_access
    def mutate(self, info, project_name, user_email):
        success = False

        integrates_dal.remove_role_to_project_dynamo(project_name, user_email,
                                                     'customeradmin')
        success = integrates_dal.remove_project_access_dynamo(
            user_email, project_name)
        removed_email = user_email if success else None
        if success:
            util.invalidate_cache(project_name)
            util.invalidate_cache(user_email)
            util.cloudwatch_log(info.context, 'Security: Removed user: {user} from {project} \
                project succesfully'.format(user=user_email, project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove user: {user}\
                from {project} project'.format(user=user_email, project=project_name))
        ret = RemoveUserAccess(success=success, removed_email=removed_email)
        return ret


class EditUser(Mutation):
    """Edit user of a given project."""

    class Arguments():
        project_name = String(required=True)
        email = String(required=True)
        organization = String(required=True)
        responsibility = String(required=True)
        role = String(required=True)
        phone_number = String(required=True)

    modified_user = Field(User)
    success = Boolean()

    @require_login
    @new_require_role
    @require_project_access
    def mutate(self, info, **query_args):
        project_name = query_args.get('project_name')
        success = False
        user_data = util.get_jwt_content(info.context)
        role = get_user_role(user_data)

        modified_user_data = {
            'email': query_args.get('email'),
            'organization': query_args.get('organization'),
            'responsibility': query_args.get('responsibility'),
            'role': query_args.get('role'),
            'phone_number': query_args.get('phone_number')
        }

        if (role == 'admin'
                and modified_user_data['role'] in ['admin', 'analyst',
                                                   'customer', 'customeradmin']) \
            or (is_customeradmin(project_name, user_data['user_email'])
                and modified_user_data['role'] in ['customer', 'customeradmin']):
            if user_domain.assign_role(
               modified_user_data['email'], modified_user_data['role']):
                modify_user_information(info.context, modified_user_data,
                                        project_name)
                success = True
            else:
                rollbar.report_message('Error: Couldn\'t update user role',
                                       'error', info.context)
        else:
            rollbar.report_message('Error: Invalid role provided: ' +
                                   modified_user_data['role'], 'error',
                                   info.context)
        if success:
            util.invalidate_cache(project_name)
            util.invalidate_cache(query_args.get('email'))
            util.cloudwatch_log(info.context, 'Security: Modified user data:{user} \
                in {project} project succesfully'.format(user=query_args.get('email'),
                                                         project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to modify user \
                data:{user} in {project} project'.format(user=query_args.get('email'),
                                                         project=project_name))
        ret = \
            EditUser(success=success,
                     modified_user=User(project_name,
                                        modified_user_data['email']))
        return ret


def modify_user_information(context, modified_user_data, project_name):
    role = modified_user_data['role']
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    organization = modified_user_data['organization']
    user_domain.update_user_attribute(email, organization.lower(), 'company')
    if responsibility and len(responsibility) <= 50:
        integrates_dal.add_project_access_dynamo(email, project_name,
                                                 'responsibility',
                                                 responsibility)
    else:
        util.cloudwatch_log(
            context,
            'Security: {email} Attempted to add responsibility to project \
                {project} bypassing validation'.format(email=email,
                                                       project=project_name))
    if phone and phone[1:].isdigit():
        user_domain.add_phone_to_user(email, phone)
    else:
        util.cloudwatch_log(
            context,
            'Security: {email} Attempted to edit user phone bypassing \
                validation'.format(email=email)
        )

    if role == 'customeradmin':
        project_domain.add_user(project_name.lower(), email.lower(), role)
    elif is_customeradmin(project_name, email):
        integrates_dal.remove_role_to_project_dynamo(project_name, email, 'customeradmin')
