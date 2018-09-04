import rollbar
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from .. import util
from ..dao import integrates_dao
from ..mailer import send_mail_repositories
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field

class Resource(ObjectType):
    """ GraphQL Entity for Project Resources """
    repositories = JSONString()
    environments = JSONString()

    def __init__(self, project_name):
        self.repositories = []
        self.environments = []

        project_info = integrates_dao.get_project_dynamo(project_name)
        for info in project_info:
            if "repositories" in info:
                self.repositories = info['repositories']

            if "environments" in info:
                self.environments = info['environments']

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

    @classmethod
    def mutate(self, args, info, resources_data, project_name):
        del args

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
            mutation_result = AddRepositories(success=True, resources=Resource(project_name))
        else:
            rollbar.report_message('Error: An error occurred adding repository', 'error', info.context)
            mutation_result = AddRepositories(success=False, resources=Resource(project_name))

        return mutation_result

class RemoveRepositories(Mutation):
    """Remove repositories of a given project."""

    class Arguments(object):
        repository_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @classmethod
    def mutate(self, args, info, repository_data, project_name):
        del args

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
                self.success = False
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove repository that does not exist')
            self.success = False

        return RemoveRepositories(success=self.success, resources=Resource(project_name))
