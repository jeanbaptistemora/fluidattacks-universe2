# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
import threading

import rollbar
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field

from ..decorators import require_login, require_role, require_project_access_gql
from .. import util
from ..dao import integrates_dao
from ..mailer import send_mail_repositories

class Resource(ObjectType):
    """ GraphQL Entity for Project Resources """
    repositories = JSONString()
    environments = JSONString()

    def __init__(self, project_name):
        self.repositories = []
        self.environments = []
        project_info = integrates_dao.get_project_dynamo(project_name)
        for item in project_info:
            if "repositories" in item:
                self.repositories = item['repositories']

            if "environments" in item:
                self.environments = item['environments']

    def resolve_repositories(self, info):
        """ Resolve repositories of the given project """
        del info
        return self.repositories

    def resolve_environments(self, info):
        """ Resolve environments of the given project """
        del info
        return self.environments

class AddRepositories(Mutation):
    """Add repositories to a given project."""

    class Arguments(object):
        resources_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def mutate(self, info, resources_data, project_name):
        success = False
        json_data = []
        email_data = []

        for repo in resources_data:
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
            email_send_thread = threading.Thread( \
                                          name="Add repositories email thread", \
                                          target=send_mail_repositories, \
                                          args=(to, context,))
            email_send_thread.start()
            success = True
        else:
            rollbar.report_message('Error: An error occurred adding repository', 'error', info.context)

        return AddRepositories(success=success, resources=Resource(project_name))

class RemoveRepositories(Mutation):
    """Remove repositories of a given project."""

    class Arguments(object):
        repository_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def mutate(self, info, repository_data, project_name):
        success = False
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
                threading.Thread( \
                  name="Remove repositories email thread", \
                  target=send_mail_repositories, \
                  args=(to, context,)).start()
                success = True
            else:
                rollbar.report_message('Error: An error occurred removing repository', 'error', info.context)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove repository that does not exist')

        return RemoveRepositories(success=success, resources=Resource(project_name))

class AddEnvironments(Mutation):
    """Add environments to a given project."""

    class Arguments(object):
        resources_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def mutate(self, info, resources_data, project_name):
        success = False
        json_data = []

        for envInfo in resources_data:
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
            email_send_thread = threading.Thread( \
                                          name="Add environments email thread", \
                                          target=send_mail_repositories, \
                                          args=(to, context,))
            email_send_thread.start()
            success = True
        else:
            rollbar.report_message('Error: An error occurred adding environments', 'error', info.context)

        return AddEnvironments(success=success, resources=Resource(project_name))

class RemoveEnvironments(Mutation):
    """Remove environments of a given project."""

    class Arguments(object):
        repository_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def mutate(self, info, repository_data, project_name):
        success = False
        environment_url = repository_data.get("urlEnv")
        env_list = integrates_dao.get_project_dynamo(project_name)[0]["environments"]
        index = -1
        cont = 0

        while index < 0 and len(env_list) > cont:
            if env_list[cont]["urlEnv"] == environment_url:
                json_data = [env_list[cont]]
                index = cont
            else:
                index = -1
            cont += 1
        if index >= 0:
            remove_env = integrates_dao.remove_list_resource_dynamo(
                "FI_projects",
                "project_name",
                project_name,
                "environments",
                index)
            if remove_env:
                to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
                context = {
                    'project': project_name.upper(),
                    'user_email': info.context.session["username"],
                    'action': 'Remove environments',
                    'resources': json_data,
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
                    .format(project=project_name)
                }
                email_send_thread = threading.Thread( \
                                              name="Remove environments email thread", \
                                              target=send_mail_repositories, \
                                              args=(to, context,))
                email_send_thread.start()
                success = True
            else:
                rollbar.report_message('Error: An error occurred removing an environment', 'error', info.context)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove an environment that does not exist')

        return RemoveEnvironments(success=success, resources=Resource(project_name))
