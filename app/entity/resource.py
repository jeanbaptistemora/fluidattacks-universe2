# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from __future__ import absolute_import
from datetime import datetime
import threading
import rollbar
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field

from __init__ import FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_CLOUDFRONT_RESOURCES_DOMAIN
from ..decorators import require_login, require_role, require_project_access_gql
from .. import util
from ..dao import integrates_dao
from ..mailer import send_mail_repositories
from ..domain import resources


INTEGRATES_URL = 'https://fluidattacks.com/integrates/dashboard'


# pylint: disable=too-many-locals
class Resource(ObjectType):
    """ GraphQL Entity for Project Resources """
    repositories = JSONString()
    environments = JSONString()
    files = JSONString()

    def __init__(self, project_name):
        self.repositories = []
        self.environments = []
        self.files = []
        project_info = integrates_dao.get_project_dynamo(project_name)
        for item in project_info:
            if 'repositories' in item:
                self.repositories = item['repositories']

            if 'environments' in item:
                self.environments = item['environments']

            if 'files' in item:
                self.files = item['files']

    def resolve_repositories(self, info):
        """ Resolve repositories of the given project """
        del info
        return self.repositories

    def resolve_environments(self, info):
        """ Resolve environments of the given project """
        del info
        return self.environments

    def resolve_files(self, info):
        """ Resolve files of the given project """
        del info
        return self.files


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
            if 'urlRepo' in repo and 'branch' in repo:
                repository = repo.get('urlRepo')
                branch = repo.get('branch')
                json_data.append({
                    'urlRepo': repository,
                    'branch': branch
                })
                email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                    .format(repository=repository, branch=branch)
                email_data.append({'urlEnv': email_text})
            else:
                rollbar.report_message('Error: \
An error occurred adding repository', 'error', info.context)
        add_repo = integrates_dao.add_list_resource_dynamo(
            'FI_projects',
            'project_name',
            project_name,
            json_data,
            'repositories'
        )
        if add_repo:
            recipients = integrates_dao.get_project_users(project_name.lower())
            mail_to = [x[0] for x in recipients if x[1] == 1]
            mail_to.append(FI_MAIL_CONTINUOUS)
            mail_to.append(FI_MAIL_PROJECTS)
            context = {
                'project': project_name.upper(),
                'user_email': info.context.session['username'],
                'action': 'Add repositories',
                'resources': email_data,
                'project_url':
                    'https://fluidattacks.com/integrates/dashboard#!/project/{project!s}/resources'
                .format(project=project_name)
            }
            email_send_thread = \
                threading.Thread(name='Add repositories email thread',
                                 target=send_mail_repositories,
                                 args=(mail_to, context,))
            email_send_thread.start()
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred adding repository', 'error', info.context)

        ret = AddRepositories(success=success,
                              resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


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
        repository = repository_data.get('urlRepo')
        branch = repository_data.get('branch')
        repo_list = \
            integrates_dao.get_project_dynamo(project_name)[0]['repositories']
        index = -1
        cont = 0
        email_data = []

        while index < 0 and len(repo_list) > cont:
            if repo_list[cont]['urlRepo'] == repository and \
                    repo_list[cont]['branch'] == branch:
                email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                    .format(repository=repository, branch=branch)
                email_data.append({'urlEnv': email_text})
                index = cont
            else:
                index = -1
            cont += 1
        if index >= 0:
            remove_repo = integrates_dao.remove_list_resource_dynamo(
                'FI_projects',
                'project_name',
                project_name,
                'repositories',
                index)
            if remove_repo:
                recipients = integrates_dao.get_project_users(
                    project_name.lower())
                mail_to = [x[0] for x in recipients if x[1] == 1]
                mail_to.append(FI_MAIL_CONTINUOUS)
                mail_to.append(FI_MAIL_PROJECTS)
                context = {
                    'project': project_name.upper(),
                    'user_email': info.context.session['username'],
                    'action': 'Remove repositories',
                    'resources': email_data,
                    'project_url':
                        INTEGRATES_URL + '#!/project/{project!s}/resources'
                    .format(project=project_name)
                }
                threading.Thread(name='Remove repositories email thread',
                                 target=send_mail_repositories,
                                 args=(mail_to, context,)).start()
                success = True
            else:
                rollbar.report_message('Error: \
An error occurred removing repository', 'error', info.context)
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to remove repository that does not exist')

        ret = RemoveRepositories(success=success,
                                 resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


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

        for env_info in resources_data:
            if 'urlEnv' in env_info:
                environment_url = env_info.get('urlEnv')
                json_data.append({
                    'urlEnv': environment_url
                })
            else:
                rollbar.report_message('Error: \
An error occurred adding environments', 'error', info.context)
        add_env = integrates_dao.add_list_resource_dynamo(
            'FI_projects',
            'project_name',
            project_name,
            json_data,
            'environments'
        )
        if add_env:
            recipients = integrates_dao.get_project_users(project_name.lower())
            mail_to = [x[0] for x in recipients if x[1] == 1]
            mail_to.append(FI_MAIL_CONTINUOUS)
            mail_to.append(FI_MAIL_PROJECTS)
            context = {
                'project': project_name.upper(),
                'user_email': info.context.session['username'],
                'action': 'Add environments',
                'resources': json_data,
                'project_url':
                    INTEGRATES_URL + '#!/project/{project!s}/resources'
                .format(project=project_name)
            }
            email_send_thread = \
                threading.Thread(name='Add environments email thread',
                                 target=send_mail_repositories,
                                 args=(mail_to, context,))
            email_send_thread.start()
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred adding environments', 'error', info.context)

        ret = AddEnvironments(success=success,
                              resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


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
        environment_url = repository_data.get('urlEnv')
        env_list = \
            integrates_dao.get_project_dynamo(project_name)[0]['environments']
        index = -1
        cont = 0

        while index < 0 and len(env_list) > cont:
            if env_list[cont]['urlEnv'] == environment_url:
                json_data = [env_list[cont]]
                index = cont
            else:
                index = -1
            cont += 1
        if index >= 0:
            remove_env = integrates_dao.remove_list_resource_dynamo(
                'FI_projects',
                'project_name',
                project_name,
                'environments',
                index)
            if remove_env:
                recipients = integrates_dao.get_project_users(
                    project_name.lower())
                mail_to = [x[0] for x in recipients if x[1] == 1]
                mail_to.append(FI_MAIL_CONTINUOUS)
                mail_to.append(FI_MAIL_PROJECTS)
                context = {
                    'project': project_name.upper(),
                    'user_email': info.context.session['username'],
                    'action': 'Remove environments',
                    'resources': json_data,
                    'project_url':
                        INTEGRATES_URL + '#!/project/{project!s}/resources'
                    .format(project=project_name)
                }
                email_send_thread = \
                    threading.Thread(name='Remove environments email thread',
                                     target=send_mail_repositories,
                                     args=(mail_to, context,))
                email_send_thread.start()
                success = True
            else:
                rollbar.report_message('Error: \
An error occurred removing an environment', 'error', info.context)
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to remove an environment that does not exist')

        ret = RemoveEnvironments(success=success, resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


class AddFiles(Mutation):
    """ Update evidence files """
    class Arguments(object):
        files_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'admin'])
    def mutate(self, info, **parameters):
        success = False
        json_data = []
        files_data = parameters['files_data']
        project_name = parameters['project_name'].lower()
        for file_info in files_data:
            json_data.append({
                'fileName': file_info.get('fileName'),
                'description': file_info.get('description'),
                'uploadDate': str(datetime.now().replace(second=0, microsecond=0))[:-3]
            })
        uploaded_file = info.context.FILES.get('document', '')
        file_id = '{project}/{file_name}'.format(
            project=project_name,
            file_name=uploaded_file
        )
        success = resources.upload_file_to_s3(uploaded_file, file_id)
        if success:
            integrates_dao.add_list_resource_dynamo(
                'FI_projects',
                'project_name',
                project_name,
                json_data,
                'files'
            )
        else:
            # The code should do nothing if the upload to S3 fails.
            pass
        ret = AddFiles(success=success, resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


class RemoveFiles(Mutation):
    """Remove files of a given project."""

    class Arguments(object):
        files_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access_gql
    def mutate(self, info, files_data, project_name):
        success = False
        file_name = files_data.get('fileName')
        file_list = \
            integrates_dao.get_project_dynamo(project_name)[0]['files']
        index = -1
        cont = 0

        while index < 0 and len(file_list) > cont:
            if file_list[cont]['fileName'] == file_name:
                index = cont
            else:
                index = -1
            cont += 1
        if index >= 0:
            file_url = project_name + '/' + file_name
            success = resources.delete_file_from_s3(file_url)
            integrates_dao.remove_list_resource_dynamo(
                'FI_projects',
                'project_name',
                project_name,
                'files',
                index)
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to remove a file that does not exist')

        ret = RemoveFiles(success=success, resources=Resource(project_name))
        util.invalidate_cache(project_name)
        return ret


class DownloadFile(Mutation):
    """ Download requested resource file """
    class Arguments(object):
        files_data = JSONString()
        project_name = String()
    success = Boolean()
    url = String()

    @require_login
    @require_role(['analyst', 'admin'])
    def mutate(self, info, **parameters):
        success = False
        file_info = parameters['files_data']
        file_url = parameters['project_name'] + "/" + file_info
        minutes_until_expire = 2
        signed_url = resources.sign_url(FI_CLOUDFRONT_RESOURCES_DOMAIN,
                                        file_url, minutes_until_expire)
        if signed_url:
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred generating signed URL', 'error', info.context)
        ret = DownloadFile(success=success, url=str(signed_url))
        return ret
