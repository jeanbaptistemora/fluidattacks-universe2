from .alert import Alert
from graphene import Field, String, ObjectType

class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert, 
                  project=String(required=True), 
                  organization=String(required=True))
    
    #pylint: disable=unused-argument
    def resolve_alert(self, info, project=None, organization=None):
        """ Resolve for alert """
        return Alert(project, organization)