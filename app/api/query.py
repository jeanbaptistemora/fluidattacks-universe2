# pylint: disable=no-self-use
from graphene import Field, List, ObjectType, String

from app import util
from app.dal import integrates_dal
from app.dal.helpers.formstack import FormstackAPI
from app.decorators import (
    get_cached, require_event_access, require_finding_access,
    require_login, require_project_access, require_role
)
from app.domain import project as project_domain
from app.entity.me import Me
from app.entity.alert import Alert
from app.entity.login import Login
from app.entity.event import Event
from app.entity.resource import Resource
from app.entity.user import User
from app.entity.finding import Finding
from app.entity.project import Project
from app.exceptions import InvalidProject


class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert,
                  project_name=String(required=True),
                  organization=String(required=True))

    event = Field(Event, identifier=String(required=True))

    events = List(Event, project_name=String(required=True))

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
    @require_project_access
    @get_cached
    def resolve_alert(self, info, project_name=None, organization=None):
        """ Resolve for alert """
        del info
        return Alert(project_name, organization)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_event_access
    @get_cached
    def resolve_event(self, info, identifier=None):
        """ Resolve for event """
        util.cloudwatch_log(info.context, 'Security: Access to \
            Event: {event_id} succesfully'.format(event_id=identifier))
        return Event(identifier, info.context)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def resolve_events(self, info, project_name=""):
        """ Resolve for eventualities """
        resp = FormstackAPI().get_eventualities(str(project_name))
        project_exist = integrates_dal.get_project_attributes_dynamo(
            project_name.lower(), ['project_name'])
        data = []
        if project_exist:
            if "submissions" in resp:
                data = [Event(i["id"], info.context)
                        for i in resp["submissions"]]
        else:
            raise InvalidProject
        return data

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_finding_access
    @get_cached
    def resolve_finding(self, info, identifier=None):
        """Resolve for finding."""
        util.cloudwatch_log(info.context, 'Security: Access to finding: '
                            '{} succesfully'.format(identifier))
        findings_loader = info.context.loaders['finding']

        return findings_loader.load(identifier)

    def resolve_login(self, info):
        """ Resolve for login info """
        user_email = util.get_jwt_content(info.context)['user_email']
        return Login(user_email)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def resolve_resources(self, info, project_name):
        """ Resolve for project resources """
        util.cloudwatch_log(info.context, 'Security: Access to \
            resources: {resources_id} succesfully'.format(resources_id=project_name))
        return Resource(project_name)

    @require_login
    @require_role(['analyst', 'customeradmin', 'admin'])
    @require_project_access
    @get_cached
    def resolve_user_data(self, info, project_name, user_email):
        """ Resolve for user data """
        del info
        return User(project_name, user_email)

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def resolve_project(self, info, project_name):
        """Resolve for projects."""
        project_name = project_name.lower()
        if project_domain.validate_project(project_name):
            util.cloudwatch_log(info.context,
                                'Security: Access to project {project} '
                                'succesfully'.format(project=project_name))
            return Project(project_name)
        else:
            raise InvalidProject()

    @require_login
    def resolve_me(self, info):
        """Resolve for current user's data """
        del info
        return Me()
