import rollbar
import threading
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from .. import util
from ..dao import integrates_dao
from graphene import ObjectType, Mutation, String, Boolean, Field
from ..services import is_customeradmin, has_responsibility, has_phone_number, has_access_to_project
from datetime import datetime
from ..mailer import send_mail_access_granted

class User(ObjectType):
    """ GraphQL Entity for Project Users """
    email = String()
    role = String()
    responsability = String()
    phone_number = String()
    organization = String()
    first_login = String()
    last_login = String()
    access = Boolean()

    def __init__(self, info, project_name, user_email):
        self.email = ""
        self.role = ""
        self.responsability = ""
        self.phone_number = ""
        self.organization = ""
        self.first_login = "-"
        self.last_login = [-1,-1]
        self.access = False

        role = info.context.session['role']
        if (role in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                role)):
            if role == "customer" and not is_customeradmin(project_name, info.context.session['username']):
                util.cloudwatch_log(info.context, 'Security: Attempted to retrieve project users without permission')
            else:
                self.access = True
                self.email=user_email
                last_login = integrates_dao.get_user_last_login_dao(user_email)
                last_login = last_login.split('.',1)[0]

                if last_login == "1111-01-01 11:11:11" or last_login == "-":
                    self.last_login=[-1,-1]
                else:
                    dates_difference = datetime.now()-datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
                    diff_last_login=[dates_difference.days,dates_difference.seconds]
                    self.last_login=diff_last_login

                self.first_login = integrates_dao.get_user_first_login_dao(user_email).split('.',1)[0]
                self.organization=integrates_dao.get_organization_dao(user_email).title()
                self.responsability = has_responsibility(project_name, user_email)
                self.phone_number = has_phone_number(user_email)
                userRole=integrates_dao.get_role_dao(user_email)

                if is_customeradmin(project_name, user_email):
                    self.role = "customer_admin"
                elif userRole == "customeradmin":
                    self.role = "customer"
                else:
                    self.role = userRole
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve project users without permission')

    def resolve_email(self, info):
        """ Resolve user email """
        del info
        return self.email.lower()

    def resolve_role(self, info):
        """ Resolve user role """
        del info
        return self.role

    def resolve_responsability(self, info):
        """ Resolve user responsability in the given project """
        del info
        return self.responsability

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

    def resolve_access(self, info):
        """ Resolve access to the current entity """
        del info
        return self.access

class GrantUserAccess(Mutation):
    """Grant access to a given project."""

    class Arguments(object):
        project_name = String()
        email = String()
        organization = String()
        responsibility = String()
        role = String()
        phone_number = String()

    granted_user = Field(User)
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, **query_args):
        del args

        project_name = query_args.get("project_name")
        role = query_args.get("role")
        email = query_args.get("email")
        self.success = False

        if (info.context.session['role'] in ['customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):
            self.access = True

            new_user_data = {
                "email": query_args.get("email"),
                "organization": query_args.get("organization"),
                "responsibility": query_args.get("responsibility"),
                "role": query_args.get("role"),
                "phone_number": query_args.get("phone_number")
            }

            if (info.context.session['role'] == 'admin'):
                if (role == 'admin' or role == 'analyst' or
                        role == 'customer' or role == 'customeradmin'):
                    if create_new_user(info.context, new_user_data, project_name):
                        self.success = True
                    else:
                        rollbar.report_message("Error: Couldn't grant access to project", 'error', info.context)
                else:
                    rollbar.report_message('Error: Invalid role provided: ' + role, 'error', info.context)
            elif is_customeradmin(project_name, info.context.session['username']):
                if (role == 'customer' or role == 'customeradmin'):
                    if create_new_user(info.context, new_user_data, project_name):
                        self.success = True
                    else:
                        rollbar.report_message("Error: Couldn't grant access to project", 'error', info.context)
                else:
                    rollbar.report_message('Error: Invalid role provided: ' + role, 'error', info.context)
            else:
                self.access = False
                util.cloudwatch_log(info.context, 'Security: Attempted to grant access to project from unprivileged role: '
                                                    + info.context.session['role'])
        else:
            self.access = False
            util.cloudwatch_log(info.context, 'Security: Attempted to grant access to project from unprivileged role: '
                                                + info.context.session['role'])

        return GrantUserAccess(success=self.success, access=self.access, granted_user=User(info, project_name, email))

def create_new_user(context, new_user_data, project_name):
    email = new_user_data['email']
    organization = new_user_data['organization']
    responsibility = new_user_data['responsibility']
    role = new_user_data['role']
    phone_number = new_user_data['phone_number']

    success = False

    if not integrates_dao.is_in_database(email):
        integrates_dao.create_user_dao(email)
    if integrates_dao.is_registered_dao(email) == '0':
        integrates_dao.register(email)
        integrates_dao.assign_role(email, role)
        integrates_dao.assign_company(email, organization)
    elif integrates_dao.is_registered_dao(email) == '1':
        integrates_dao.assign_role(email, role)
    if responsibility and len(responsibility) <= 50:
        integrates_dao.add_project_access_dynamo(email, project_name, "responsibility", responsibility)
    else:
        util.cloudwatch_log(
            context,
            'Security: ' + context.session['username'] + 'Attempted to add ' +
            'responsibility to project ' + project_name + ' without validation'
        )
    if phone_number:
        if phone_number[1:].isdigit():
            integrates_dao.add_phone_to_user_dynamo(email, phone_number)
    if role == 'customeradmin':
        integrates_dao.add_user_to_project_dynamo(project_name.lower(), email.lower(), role)
    if integrates_dao.add_access_to_project_dao(email, project_name):
        description = integrates_dao.get_project_description(project_name)
        project_url = 'https://fluidattacks.com/integrates/dashboard#!/project/' \
                      + project_name.lower() + '/indicators'
        to = [email]
        context = {
           'admin': context.session["username"],
           'project': project_name,
           'project_description': description,
           'project_url': project_url,
        }
        email_send_thread = threading.Thread( \
                                      name="Access granted email thread", \
                                      target=send_mail_access_granted, \
                                      args=(to, context,))
        email_send_thread.start()
        success = True
    return success

class RemoveUserAccess(Mutation):
    """Remove user of a given project."""

    class Arguments(object):
        project_name = String()
        user_email = String()

    removed_email = String()
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, project_name, user_email):
        del args

        self.success = False
        role = info.context.session['role']
        if (role in ['customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                role)):
            self.access = True
            if (role == "customer" and not is_customeradmin(project_name, info.context.session['username'])):
                util.cloudwatch_log(info.context, 'Security: Attempted to remove project users without permission')
            else:
                integrates_dao.remove_role_to_project_dynamo(project_name, user_email, "customeradmin")
                is_user_removed_dao = integrates_dao.remove_access_project_dao(user_email, project_name)
                is_user_removed_dynamo = integrates_dao.remove_project_access_dynamo(user_email, project_name)
                self.success = is_user_removed_dao and is_user_removed_dynamo
                self.removed_email = user_email if self.success else None
        else:
            self.access = False
            util.cloudwatch_log(info.context, 'Security: Attempted to remove project users without permission')

        return RemoveUserAccess(success=self.success, access=self.access, removed_email=self.removed_email)

class EditUser(Mutation):
    """Edit user of a given project."""

    class Arguments(object):
        project_name = String(required=True)
        email = String(required=True)
        organization = String(required=True)
        responsibility = String(required=True)
        role = String(required=True)
        phone_number = String(required=True)

    modified_user = Field(User)
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, **query_args):
        del args

        role = query_args.get("role")
        email = query_args.get("email")
        project_name = query_args.get("project_name")
        self.success = False

        if (info.context.session['role'] in ['customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):
            self.access = True

            modified_user_data = {
                "email": query_args.get("email"),
                "organization": query_args.get("organization"),
                "responsibility": query_args.get("responsibility"),
                "role": query_args.get("role"),
                "phone_number": query_args.get("phone_number")
            }

            if info.context.session['role'] == 'admin':
                if (role == 'admin' or role == 'analyst' or
                        role == 'customer' or role == 'customeradmin'):
                    if integrates_dao.assign_role(email, role) is None:
                        modify_user_information(info.context, modified_user_data, project_name)
                        self.success = True
                    else:
                        rollbar.report_message("Error: Couldn't update user role", 'error', info.context)
                else:
                    rollbar.report_message('Error: Invalid role provided: ' + role, 'error', info.context)
            elif is_customeradmin(project_name, info.context.session['username']):
                if role == 'customer' or role == 'customeradmin':
                    if integrates_dao.assign_role(email, role) is None:
                        modify_user_information(info.context, modified_user_data, project_name)
                        self.success = True
                    else:
                        rollbar.report_message("Error: Couldn't update user role", 'error', info.context)
                else:
                    rollbar.report_message('Error: Invalid role provided: ' + role, 'error', info.context)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to edit project users info without permission')

        return EditUser(success=self.success, access=self.access, modified_user=User(info, project_name, email))

def modify_user_information(context, modified_user_data, project_name):
    role = modified_user_data['role']
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    organization = modified_user_data['organization']
    integrates_dao.assign_company(email, organization.lower())
    if responsibility and len(responsibility) <= 50:
        integrates_dao.add_project_access_dynamo(email, project_name, "responsibility", responsibility)
    else:
        util.cloudwatch_log(
            context,
            'Security: ' + context.session['username'] + 'Attempted to add ' +
            'responsibility to project ' + project_name + ' bypassing validation'
        )
    if phone and phone[1:].isdigit():
        integrates_dao.add_phone_to_user_dynamo(email, phone)
    else:
        util.cloudwatch_log(
            context,
            'Security: ' + context.session['username'] + 'Attempted to ' +
            'edit user phone bypassing validation'
        )

    if role == 'customeradmin':
        integrates_dao.add_user_to_project_dynamo(project_name.lower(), email.lower(), role)
    elif is_customeradmin(project_name, email):
        integrates_dao.remove_role_to_project_dynamo(project_name, email, "customeradmin")
