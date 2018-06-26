from .alert import Alert
from .eventuality import Eventuality
# pylint: disable=F0401
from app.api.formstack import FormstackAPI
from graphene import Field, String, ObjectType, List

class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert, 
                  project=String(required=True), 
                  organization=String(required=True))
    
    eventuality = Field(Eventuality,
                        submitID=String(required=True))
    
    eventualities = List(Eventuality,
                        project=String(required=True))

    #pylint: disable=unused-argument
    def resolve_alert(self, info, project=None, organization=None):
        """ Resolve for alert """
        return Alert(project, organization)
    #pylint: disable=unused-argument
    def resolve_eventuality(self, info, submitID=None):
        """ Resolve for eventuality """
        return Eventuality(submitID)
    #pylint: disable=unused-argument
    def resolve_eventualities(self, info, project=""):
        """ Resolve for eventualities """
        resp = FormstackAPI().get_eventualities(str(project))
        data = []
        if "submissions" in resp:
            data = [Eventuality(i["id"]) for i in resp["submissions"]]
        return data