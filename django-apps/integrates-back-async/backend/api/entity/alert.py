# pylint: disable=import-error

from ariadne import ObjectType

from backend.api.entity.query import QUERY

ALERT = ObjectType('Alert')


@QUERY.field('alert')
def resolve_alert(*_, project_name, organization):
    return Alert(project_name, organization)


class Alert():
    """ Dynamo Alert Class """
    message = str()
    project = str()
    organization = str()
    status = int()

    def __init__(self, project_name, organization):
        """ Class constructor """
        self.message, self.project = "", ""
        self.organization, self.status = "", 0
        resp = [
            {
                'message': 'unittest',
                'project_name': 'unittesting',
                'company_name': 'fluid',
                'status_act': 0
            }
        ]
        # Mock response
        if resp and project_name and organization:
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
