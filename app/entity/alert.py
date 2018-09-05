""" GraphQL Entity for Dynamo Alerts """
# pylint: disable=F0401
from app import util
from app.dao import integrates_dao
from graphene import Int, String, ObjectType, Boolean
from app.services import has_access_to_project

class Alert(ObjectType):
    """ Dynamo Alert Class """
    message = String()
    project = String()
    organization = String()
    status = Int()
    access = Boolean()

    def __init__(self, info, project_name, organization):
        """ Class constructor """
        self.message, self.project = "", ""
        self.organization, self.status = "", 0
        self.access = False

        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):

            self.access = True
            project = str(project_name)
            organization = str(organization)
            resp = integrates_dao.get_company_alert_dynamo(organization, project)
            if resp:
                self.message = resp[0]['message']
                self.project = resp[0]['project_name']
                self.organization = resp[0]['company_name']
                self.status = resp[0]['status_act']
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve alerts info without permission')

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

    def resolve_access(self, info):
        """ Resolve access to the current entity """
        del info
        return self.access
