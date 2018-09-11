from .alert import Alert
from .login import Login
from .events import Events
from .resource import Resource
# pylint: disable=F0401
from app.api.formstack import FormstackAPI
from graphene import Field, String, ObjectType, List

class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert,
                  project=String(required=True),
                  organization=String(required=True))

    event = Field(Events,
                        identifier=String(required=True))

    events = List(Events,
                        identifier=String(required=True))

    login = Field(Login)

    resources = Field(Resource, project_name=String(required=True))

    def resolve_alert(self, info, project=None, organization=None):
        """ Resolve for alert """
        return Alert(info, project, organization)

    def resolve_event(self, info, identifier=None):
        """ Resolve for event """
        del info
        return Events(identifier)

    def resolve_events(self, info, identifier=""):
        """ Resolve for eventualities """
        del info
        resp = FormstackAPI().get_eventualities(str(identifier))
        data = []
        if "submissions" in resp:
            data = [Events(i["id"]) for i in resp["submissions"]]
        return data

    def resolve_login(self, info):
        """ Resolve for login info """
        user_email = info.context.session["username"]
        return Login(user_email, info.context.session)

    def resolve_resources(self, info, project_name):
        return Resource(info, project_name)
