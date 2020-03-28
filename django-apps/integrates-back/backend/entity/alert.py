""" GraphQL Entity for Dynamo Alerts """
# pylint: disable=F0401
# pylint: disable=super-init-not-called
from graphene import Boolean, Int, Mutation, ObjectType, String
from backend.decorators import require_login, enforce_group_level_auth
from backend.domain import alert as alert_domain

from backend import util


class Alert(ObjectType):
    """ Dynamo Alert Class """
    message = String()
    project = String()
    organization = String()
    status = Int()

    def __init__(self, project_name, organization):
        """ Class constructor """
        self.message, self.project = "", ""
        self.organization, self.status = "", 0
        project = str(project_name)
        organization = str(organization)
        resp = alert_domain.get_company_alert(organization, project)
        if resp:
            self.message = resp[0]['message']
            self.project = resp[0]['project_name']
            self.organization = resp[0]['company_name']
            self.status = resp[0]['status_act']

    def resolve_message(self, info):
        """ Resolve message attribute """
        del info
        return self.message

    def resolve_project(self, info):
        """ Resolve project attribute """
        del info
        return self.project

    def resolve_organization(self, info):
        """ Resolve organization attribute """
        del info
        return self.organization

    def resolve_status(self, info):
        """ Resolve status attribute """
        del info
        return self.status


class SetAlert(Mutation):

    class Arguments():
        company = String(required=True)
        message = String(required=True)
        project_name = String(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @enforce_group_level_auth
    def mutate(_, info, company, message, project_name):
        success = alert_domain.set_company_alert(
            company, message, project_name)
        if success:
            util.cloudwatch_log(
                info.context, f'Security: Set alert of {company}')
        return SetAlert(success=success)
