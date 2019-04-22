# pylint: disable=no-self-use
from graphene import Field, String, ObjectType, List

from app.api.formstack import FormstackAPI
from app.entity.me import Me
from app.entity.alert import Alert
from app.entity.login import Login
from app.entity.events import Events
from app.entity.resource import Resource
from app.entity.user import User
from app.entity.finding import Finding
from app.entity.project import Project
# pylint: disable=F0401
from app.decorators import (
    require_login, require_role,
    require_project_access_gql,
    require_finding_access_gql, get_cached,
    require_event_access_gql
)


class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert,
                  project_name=String(required=True),
                  organization=String(required=True))

    event = Field(Events, identifier=String(required=True))

    events = List(Events, project_name=String(required=True))

    finding = Field(Finding, identifier=String(required=True))

    login = Field(Login)

    resources = Field(Resource, project_name=String(required=True))

    user_data = Field(User, project_name=String(required=True),
                      user_email=String(required=True))

    project = Field(Project, project_name=String(required=True))

    # pylint: disable=invalid-name
    me = Field(Me)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    @get_cached
    def resolve_alert(self, info, project_name=None, organization=None):
        """ Resolve for alert """
        del info
        return Alert(project_name, organization)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_event_access_gql
    @get_cached
    def resolve_event(self, info, identifier=None):
        """ Resolve for event """
        del info
        return Events(identifier)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def resolve_events(self, info, project_name=""):
        """ Resolve for eventualities """
        del info
        resp = FormstackAPI().get_eventualities(str(project_name))
        data = []
        if "submissions" in resp:
            data = [Events(i["id"]) for i in resp["submissions"]]
        return data

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_finding_access_gql
    @get_cached
    def resolve_finding(self, info, identifier=None):
        """Resolve for finding."""
        return Finding(info, identifier)

    def resolve_login(self, info):
        """ Resolve for login info """
        user_email = info.context.session["username"]
        return Login(user_email, info.context.session)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def resolve_resources(self, info, project_name):
        """ Resolve for project resources """
        del info
        return Resource(project_name)

    @require_login
    @require_role(['analyst', 'customeradmin', 'admin'])
    @require_project_access_gql
    @get_cached
    def resolve_user_data(self, info, project_name, user_email):
        """ Resolve for user data """
        del info
        return User(project_name, user_email)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def resolve_project(self, info, project_name):
        """Resolve for projects."""
        del info
        return Project(project_name)

    @require_login
    def resolve_me(self, info):
        """Resolve for current user's data """
        del info
        return Me()
