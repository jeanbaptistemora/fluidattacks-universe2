# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from datetime import datetime
import rollbar
from mixpanel import Mixpanel
from graphql import GraphQLError
from graphene import ObjectType, JSONString, Mutation, String, Boolean, Field
from graphene_file_upload.scalars import Upload
from django.conf import settings

from __init__ import FI_CLOUDFRONT_RESOURCES_DOMAIN
from ..decorators import (
    require_login, require_role, require_project_access, get_entity_cache
)
from .. import util
from ..dal import integrates_dal
from ..domain import resources
from ..exceptions import ErrorUploadingFileS3, InvalidFileSize, InvalidProject


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
        project_name = project_name.lower()
        success = False
        user_email = util.get_jwt_content(info.context)['user_email']
        if res_type == 'repository':
            res_id = 'urlRepo'
            res_name = 'repositories'
        elif res_type == 'environment':
            res_id = 'urlEnv'
            res_name = 'environments'
        json_data = []
        for res in resource_data:
            if res_id in res:
                new_state = {
                    'user': user_email,
                    'date': util.format_comment_date(
                        datetime.today().strftime('%Y-%m-%d %H:%M:%S')),
                    'state': 'ACTIVE'
                }
                if res_type == 'repository':
                    res_object = {
                        'urlRepo': res.get('urlRepo'),
                        'branch': res.get('branch'),
                        'protocol': res.get('protocol'),
                        'uploadDate': str(datetime.now().replace(second=0, microsecond=0))[:-3],
                        'historic_state': [new_state],
                    }
                elif res_type == 'environment':
                    res_object = {
                        'urlEnv': res.get('urlEnv'),
                        'historic_state': [new_state],
                    }
                json_data.append(res_object)
            else:
                rollbar.report_message('Error: \
An error occurred adding repository', 'error', info.context)
        add_repo = integrates_dal.add_list_resource_dynamo(
            'FI_projects',
            'project_name',
            project_name,
            json_data,
            res_name
        )
        if add_repo:
            resources.send_mail(project_name,
                                user_email,
                                json_data,
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
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, **parameters):
        success = False
        json_data = []
        files_data = parameters['files_data']
        project_name = parameters['project_name'].lower()
        user_email = util.get_jwt_content(info.context)['user_email']
        for file_info in files_data:
            json_data.append({
                'fileName': file_info.get('fileName'),
                'description': file_info.get('description'),
                'uploadDate': str(datetime.now().replace(second=0, microsecond=0))[:-3],
                'uploader': user_email,
            })
        uploaded_file = info.context.FILES['1']
        file_id = '{project}/{file_name}'.format(
            project=project_name,
            file_name=uploaded_file
        )
        try:
            file_size = 100
            resources.validate_file_size(uploaded_file, file_size)
        except InvalidFileSize:
            raise GraphQLError('File exceeds the size limits')
        files = integrates_dal.get_project_attributes_dynamo(project_name, ['files'])
        project_files = files.get('files')
        if project_files:
            contains_repeated = [f.get('fileName')
                                 for f in project_files
                                 if f.get('fileName') == uploaded_file.name]
            if contains_repeated:
                raise GraphQLError('File already exist')
        else:
            # Project doesn't have files
            pass
        if util.is_valid_file_name(uploaded_file):
            try:
                resources.save_file(uploaded_file, file_id)
                integrates_dal.add_list_resource_dynamo(
                    'FI_projects',
                    'project_name',
                    project_name,
                    json_data,
                    'files'
                )
                resources.send_mail(project_name,
                                    user_email,
                                    json_data,
                                    'added',
                                    'file')
                success = True
            except ErrorUploadingFileS3:
                raise GraphQLError('Error uploading file')
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
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, files_data, project_name):
        success = False
        file_name = files_data.get('fileName')
        file_list = \
            integrates_dal.get_project_dynamo(project_name)[0]['files']
        index = -1
        cont = 0
        user_email = util.get_jwt_content(info.context)['user_email']

        while index < 0 and len(file_list) > cont:
            if file_list[cont]['fileName'] == file_name:
                index = cont
                json_data = [file_list[cont]]
            else:
                index = -1
            cont += 1
        if index >= 0:
            file_url = '{project}/{file_name}'.format(
                project=project_name.lower(),
                file_name=file_name
            )
            success = resources.remove_file(file_url)
            integrates_dal.remove_list_resource_dynamo(
                'FI_projects',
                'project_name',
                project_name,
                'files',
                index)
            resources.send_mail(project_name,
                                user_email,
                                json_data,
                                'removed',
                                'file')
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
        file_url = project_name + "/" + file_info
        minutes_until_expire = 1.0 / 6
        signed_url = resources.sign_url(FI_CLOUDFRONT_RESOURCES_DOMAIN,
                                        file_url, minutes_until_expire)
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
