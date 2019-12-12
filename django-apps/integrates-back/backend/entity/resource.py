# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import rollbar
from mixpanel import Mixpanel
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field
from graphene_file_upload.scalars import Upload
from django.conf import settings


from backend.decorators import (
    require_login, require_role, require_project_access, get_entity_cache
)
from backend.domain import resources

from app import util
from app.dal import integrates_dal
from app.exceptions import InvalidProject

INTEGRATES_URL = 'https://fluidattacks.com/integrates/dashboard'


# pylint: disable=too-many-locals
class Resource(ObjectType):
    """ GraphQL Entity for Project Resources """
    project_name = ''
    repositories = JSONString()
    environments = JSONString()
    files = JSONString()

    def __init__(self, project_name):
        self.project_name = project_name
        self.repositories = []
        self.environments = []
        self.files = []
        project_exist = integrates_dal.get_project_attributes_dynamo(
            project_name.lower(), ['project_name'])
        if project_exist:
            project_info = integrates_dal.get_project_attributes_dynamo(
                project_name.lower(), ['repositories', 'environments', 'files'])
            if project_info:
                self.repositories = project_info.get('repositories', [])
                self.environments = project_info.get('environments', [])
                self.files = project_info.get('files', [])
            else:
                # Project does not have resources
                pass
        else:
            raise InvalidProject

    def __str__(self):
        return self.project_name + '_resources'

    @get_entity_cache
    def resolve_repositories(self, info):
        """ Resolve repositories of the given project """
        del info
        return self.repositories

    @get_entity_cache
    def resolve_environments(self, info):
        """ Resolve environments of the given project """
        del info
        return self.environments

    @get_entity_cache
    def resolve_files(self, info):
        """ Resolve files of the given project """
        del info
        return self.files


class AddResources(Mutation):
    """Add resources (repositories + environments) to a given project."""

    class Arguments():
        resource_data = JSONString()
        project_name = String()
        res_type = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, resource_data, project_name, res_type):
        success = False
        user_email = util.get_jwt_content(info.context)['user_email']
        add_res = resources.create_resource(resource_data, project_name, res_type, user_email)
        if add_res:
            resources.send_mail(project_name,
                                user_email,
                                resource_data,
                                'added',
                                res_type)
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred adding resource', 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Added resources to \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to add resources \
                from {project} project'.format(project=project_name))
        ret = AddResources(success=success,
                           resources=Resource(project_name))
        return ret


class UpdateResources(Mutation):
    """Remove resources (repositories + environments) of a given project."""

    class Arguments():
        resource_data = JSONString()
        project_name = String()
        res_type = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, resource_data, project_name, res_type):
        success = False
        user_email = util.get_jwt_content(info.context)['user_email']
        update_res = resources.update_resource(resource_data, project_name, res_type, user_email)
        if update_res:
            resources.send_mail(project_name,
                                user_email,
                                [resource_data],
                                'activated'
                                if resource_data.get('state') == 'INACTIVE'
                                else 'deactivated',
                                res_type)
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred updating resource', 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Updated resources from \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to update resources \
                from {project} project'.format(project=project_name))
        ret = UpdateResources(success=success,
                              resources=Resource(project_name))
        return ret


class AddFiles(Mutation):
    """ Update evidence files """
    class Arguments():
        file = Upload(required=True)
        files_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, **parameters):
        success = False
        files_data = parameters['files_data']
        uploaded_file = info.context.FILES['1']
        project_name = parameters['project_name']
        user_email = util.get_jwt_content(info.context)['user_email']
        add_file = resources.create_file(files_data,
                                         uploaded_file,
                                         project_name,
                                         user_email)
        if add_file:
            resources.send_mail(project_name,
                                user_email,
                                files_data,
                                'added',
                                'file')

            success = True
        else:
            rollbar.report_message('Error: \
An error occurred uploading file', 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Added evidence files to \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to add evidence files \
                from {project} project'.format(project=project_name))
        ret = AddFiles(success=success, resources=Resource(project_name))
        return ret


class RemoveFiles(Mutation):
    """Remove files of a given project."""

    class Arguments():
        files_data = JSONString()
        project_name = String()
    resources = Field(Resource)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, files_data, project_name):
        success = False
        file_name = files_data.get('fileName')
        user_email = util.get_jwt_content(info.context)['user_email']
        remove_file = resources.remove_file(file_name, project_name)
        if remove_file:
            resources.send_mail(project_name,
                                user_email,
                                files_data,
                                'removed',
                                'file')
            success = True
        else:
            rollbar.report_message('Error: \
An error occurred removing file', 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Removed Files from \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove files \
                from {project} project'.format(project=project_name))
        ret = RemoveFiles(success=success, resources=Resource(project_name))
        return ret


class DownloadFile(Mutation):
    """ Download requested resource file """
    class Arguments():
        files_data = JSONString()
        project_name = String()
    success = Boolean()
    url = String()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, **parameters):
        success = False
        file_info = parameters['files_data']
        project_name = parameters['project_name'].lower()
        user_email = util.get_jwt_content(info.context)['user_email']
        signed_url = resources.download_file(file_info, project_name)
        if signed_url:
            msg = 'Security: Downloaded file {file_name} in project {project} succesfully'\
                .format(project=project_name, file_name=parameters['files_data'])
            util.cloudwatch_log(info.context, msg)
            mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
            mp_obj.track(user_email, 'DownloadProjectFile', {
                'Project': project_name.upper(),
                'Email': user_email,
                'FileName': parameters['files_data'],
            })
            success = True
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to download file {file_name} \
                in project {project}'.format(project=project_name,
                                             file_name=parameters['files_data']))
            rollbar.report_message('Error: \
An error occurred generating signed URL', 'error', info.context)
        ret = DownloadFile(success=success, url=str(signed_url))
        return ret
