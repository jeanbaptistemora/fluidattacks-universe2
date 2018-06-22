""" GraphQL Entity for Dynamo Alerts """
# pylint: disable=F0401
from app.dao import integrates_dao
from graphene import Int, String, ObjectType


class Alert(ObjectType):
    """ Dynamo Alert Class """
    message = String()
    project = String()
    organization = String()
    status = Int()

    def __init__(self, project, organization):
        """ Class constructor """
        self.message, self.project = "", ""
        self.organization, self.status = "", 0
        project = str(project)
        organization = str(organization)
        resp = integrates_dao.get_company_alert_dynamo(organization, project)
        if resp:
            self.message = resp[0]['message']
            self.project = resp[0]['project_name']
            self.organization = resp[0]['company_name']
            self.status = resp[0]['status_act']
    #pylint: disable=unused-argument
    def resolve_message(self, info):
        """ Resolve message attribute """
        return self.message
    #pylint: disable=unused-argument
    def resolve_project(self, info):
        """ Resolve project attribute """
        return self.project
    #pylint: disable=unused-argument
    def resolve_organization(self, info):
        """ Resolve organization attribute """
        return self.organization
    #pylint: disable=unused-argument
    def resolve_status(self, info):
        """ Resolve status attribute """
        return self.status