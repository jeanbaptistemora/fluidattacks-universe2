# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from .. import util
from ..dao import integrates_dao
from graphene import ObjectType, String, Boolean
from ..services import is_customeradmin, has_responsibility, has_phone_number, has_access_to_project
from datetime import datetime

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

                if last_login == "1111-01-01 11:11:11":
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
        return self.email

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
