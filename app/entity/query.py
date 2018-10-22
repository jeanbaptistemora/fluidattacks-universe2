# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from .alert import Alert
from .login import Login
from .events import Events
from .resource import Resource
from .user import User
from ..dao import integrates_dao
from .. import util
from .finding import Finding
# pylint: disable=F0401
from app.api.formstack import FormstackAPI
from graphene import Field, String, ObjectType, List
from ..decorators import require_login, require_role, require_project_access_gql

class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert,
                  project_name=String(required=True),
                  organization=String(required=True))

    event = Field(Events,
                        identifier=String(required=True))

    events = List(Events,
                        identifier=String(required=True))

    finding = Field(Finding, identifier=String(required=True))

    login = Field(Login)

    resources = Field(Resource, project_name=String(required=True))

    project_users = List(User, project_name=String(required=True))

    user_data = Field(User,
        project_name=String(required=True),
        user_email=String(required=True)
    )

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def resolve_alert(self, info, project_name=None, organization=None):
        """ Resolve for alert """
        del info
        return Alert(project_name, organization)

    def resolve_event(self, info, identifier=None):
        """ Resolve for event """
        return Events(info, identifier)

    def resolve_events(self, info, identifier=""):
        """ Resolve for eventualities """
        resp = FormstackAPI().get_eventualities(str(identifier))
        data = []
        if "submissions" in resp:
            data = [Events(info, i["id"]) for i in resp["submissions"]]
        return data

    def resolve_finding(self, info, identifier=None):
        """Resolve for finding."""
        return Finding(info, identifier)

    def resolve_login(self, info):
        """ Resolve for login info """
        user_email = info.context.session["username"]
        return Login(user_email, info.context.session)

    def resolve_resources(self, info, project_name):
        return Resource(info, project_name)

    def resolve_project_users(self, info, project_name):
        initialEmails = integrates_dao.get_project_users(project_name.lower())
        initialEmailsList = [x[0] for x in initialEmails if x[1] == 1]
        userEmailList = util.user_email_filter(
            initialEmailsList,
            info.context.session['username']
        )
        if userEmailList:
            data = [User(info, project_name, user_email) for user_email in userEmailList]
        else:
            data = []
        return data

    def resolve_user_data(self, info, project_name, user_email):
        return User(info, project_name, user_email)
