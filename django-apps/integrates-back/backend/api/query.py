# pylint: disable=no-self-use
from graphene import Field, List, ObjectType, String

from backend.decorators import (
    get_cached, require_event_access, require_finding_access,
    require_login, require_project_access, new_require_role
)
from backend.domain import project as project_domain
from backend.entity.me import Me
from backend.entity.alert import Alert
from backend.entity.event import Event
from backend.entity.resource import Resource
from backend.entity.user import User
from backend.entity.finding import Finding
from backend.entity.project import Project
from backend.entity.internal_project import InternalProject

from backend import services
from backend import util
from backend.exceptions import InvalidProject


class Query(ObjectType):
    """ Graphql Class """
    alert = Field(Alert,
                  project_name=String(required=True),
                  organization=String(required=True))

    event = Field(Event, identifier=String(required=True))

    events = List(Event, project_name=String(required=True))

    finding = Field(Finding, identifier=String(required=True))

    internal_project_names = Field(InternalProject)

    alive_projects = List(Project)

    resources = Field(Resource, project_name=String(required=True))

    user = Field(User, project_name=String(required=True),
                 user_email=String(required=True))

    user_list_projects = Field(User.list_projects,
                               user_email=String(required=True))

    project = Field(Project, project_name=String(required=True))

    # pylint: disable=invalid-name
    me = Field(Me)

    @require_login
    @new_require_role
    @require_project_access
    @get_cached
    def resolve_alert(self, info, project_name=None, organization=None):
        """ Resolve for alert """
        del info
        return Alert(project_name, organization)

    @require_login
    @new_require_role
    @require_event_access
    @get_cached
    def resolve_event(self, info, identifier=None):
        """ Resolve for event """
        util.cloudwatch_log(
            info.context,
            f'Security: Access to Event: {identifier} succesfully')
        events_loader = info.context.loaders['event']

        return events_loader.load(identifier)

    @require_login
    @new_require_role
    @require_finding_access
    @get_cached
    def resolve_finding(self, info, identifier=None):
        """Resolve for finding."""
        util.cloudwatch_log(info.context, 'Security: Access to finding: '
                            '{} succesfully'.format(identifier))
        findings_loader = info.context.loaders['finding']

        return findings_loader.load(identifier)

    @require_login
    @new_require_role
    @require_project_access
    def resolve_resources(self, info, project_name):
        """ Resolve for project resources """
        util.cloudwatch_log(info.context, 'Security: Access to \
            resources: {resources_id} succesfully'.format(resources_id=project_name))
        return Resource(project_name)

    @require_login
    @new_require_role
    @require_project_access
    @get_cached
    def resolve_user(self, info, project_name, user_email):
        """ Resolve for user data """
        role = services.get_user_role(util.get_jwt_content(info.context))
        return User(project_name, user_email, role=role)

    @require_login
    @new_require_role
    def resolve_user_list_projects(self, info, user_email):
        del info
        return User(None, user_email).list_projects

    @require_login
    @new_require_role
    @require_project_access
    def resolve_project(self, info, project_name):
        """Resolve for projects."""
        project_name = project_name.lower()
        user_email = util.get_jwt_content(info.context)['user_email']
        if project_domain.is_request_deletion_user(project_name, user_email):
            util.cloudwatch_log(info.context,
                                f'Security: Access to project {project_name} succesfully')
            return Project(
                project_name,
                description=project_domain.get_description(project_name))
        raise InvalidProject()

    @require_login
    @new_require_role
    def resolve_internal_project_names(self, info):
        """Resolve for internal project names"""
        del info
        return InternalProject()

    @require_login
    @new_require_role
    def resolve_alive_projects(self, info):
        """Resolve for ACTIVE and SUSPENDED projects"""
        del info
        alive_projects = project_domain.get_alive_projects()
        return [Project(project) for project in alive_projects]

    @require_login
    def resolve_me(self, info):
        """Resolve for current user's data """
        del info
        return Me()
