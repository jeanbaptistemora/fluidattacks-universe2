import rollbar
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from .. import util
from ..dao import integrates_dao
from ..mailer import send_mail_repositories
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field
from ..services import has_access_to_project

class Resource(ObjectType):
    """ GraphQL Entity for Project Resources """
    repositories = JSONString()
    environments = JSONString()
    access = Boolean()

    def __init__(self, info, project_name):
        self.repositories = []
        self.environments = []
        self.access = False

        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):

            self.access = True
            project_info = integrates_dao.get_project_dynamo(project_name)
            for item in project_info:
                if "repositories" in item:
                    self.repositories = item['repositories']

                if "environments" in item:
                    self.environments = item['environments']
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve project info without permission')

    def resolve_repositories(self, info):
        """ Resolve repositories of the given project """
        del info
        return self.repositories

    def resolve_environments(self, info):
        """ Resolve environments of the given project """
        del info
        return self.environments

    def resolve_access(self, info):
        """ Resolve access to the current entity """
        del info
        return self.access

class AddRepositories(Mutation):
    """Add repositories to a given project."""

    class Arguments(object):
        resources_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, resources_data, project_name):
        del args

        self.success = False
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):

            self.access = True
            json_data = []
            email_data = []
            for repo in resources_data.get("repositories"):
                if "repository" in repo and "branch" in repo:
                    repository = repo.get("repository")
                    branch = repo.get("branch")
                    json_data.append({
                        'urlRepo': repository,
                        'branch': branch
                    })
                    email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                        .format(repository=repository, branch=branch)
                    email_data.append({"urlEnv": email_text})
                else:
                    rollbar.report_message('Error: An error occurred adding repository', 'error', info.context)
            add_repo = integrates_dao.add_list_resource_dynamo(
                "FI_projects",
                "project_name",
                project_name,
                json_data,
                "repositories"
            )
            if add_repo:
                to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
                context = {
                    'project': project_name.upper(),
                    'user_email': info.context.session["username"],
                    'action': 'Add repositories',
                    'resources': email_data,
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
                    .format(project=project_name)
                }
                send_mail_repositories(to, context)
                self.success = True
            else:
                rollbar.report_message('Error: An error occurred adding repository', 'error', info.context)
        else:
            self.access = False

        return AddRepositories(success=self.success, access=self.access, resources=Resource(info, project_name))

class RemoveRepositories(Mutation):
    """Remove repositories of a given project."""

    class Arguments(object):
        repository_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, repository_data, project_name):
        del args

        self.success = False
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):

            self.access = True
            repository = repository_data.get("urlRepo")
            branch = repository_data.get("branch")
            repo_list = integrates_dao.get_project_dynamo(project_name)[0]["repositories"]
            index = -1
            cont = 0
            email_data = []
            while index < 0 and len(repo_list) > cont:
                if repo_list[cont]["urlRepo"] == repository and repo_list[cont]["branch"] == branch:
                    email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                        .format(repository=repository, branch=branch)
                    email_data.append({"urlEnv": email_text})
                    index = cont
                else:
                    index = -1
                cont += 1
            if index >= 0:
                remove_repo = integrates_dao.remove_list_resource_dynamo(
                    "FI_projects",
                    "project_name",
                    project_name,
                    "repositories",
                    index)
                if remove_repo:
                    to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
                    context = {
                        'project': project_name.upper(),
                        'user_email': info.context.session["username"],
                        'action': 'Remove repositories',
                        'resources': email_data,
                        'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
                        .format(project=project_name)
                    }
                    send_mail_repositories(to, context)
                    self.success = True
                else:
                    rollbar.report_message('Error: An error occurred removing repository', 'error', info.context)
            else:
                util.cloudwatch_log(info.context, 'Security: Attempted to remove repository that does not exist')
        else:
            self.access = False

        return RemoveRepositories(success=self.success, access=self.access, resources=Resource(info, project_name))

class AddEnvironments(Mutation):
    """Add environments to a given project."""

    class Arguments(object):
        resources_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()
    access = Boolean()

    @classmethod
    def mutate(self, args, info, resources_data, project_name):
        del args

        self.success = False
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name,
                info.context.session['role'])):

            self.access = True
            json_data = []
            for envInfo in resources_data.get("environments"):
                if "environment" in envInfo:
                    environment_url = envInfo.get("environment")
                    json_data.append({
                        'urlEnv': environment_url
                    })
                else:
                    rollbar.report_message('Error: An error occurred adding environments', 'error', info.context)
            add_env = integrates_dao.add_list_resource_dynamo(
                "FI_projects",
                "project_name",
                project_name,
                json_data,
                "environments"
            )
            if add_env:
                to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
                context = {
                    'project': project_name.upper(),
                    'user_email': info.context.session["username"],
                    'action': 'Add environments',
                    'resources': json_data,
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
                    .format(project=project_name)
                }
                send_mail_repositories(to, context)
                self.success = True
            else:
                rollbar.report_message('Error: An error occurred adding environments', 'error', info.context)
        else:
            self.access = False

        return AddEnvironments(success=self.success, access=self.access, resources=Resource(info, project_name))
