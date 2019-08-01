""" GraphQL Entity for Dynamo Alerts """
# pylint: disable=F0401
# pylint: disable=super-init-not-called
from app.dal import integrates_dal
from graphene import Int, String, ObjectType


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
        resp = integrates_dal.get_company_alert_dynamo(organization, project)
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
