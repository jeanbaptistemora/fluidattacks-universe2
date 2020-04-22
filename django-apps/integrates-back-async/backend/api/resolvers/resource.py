# pylint: disable=import-error

from typing import Any, Dict, List, cast
import asyncio
import re
import sys

import rollbar
from asgiref.sync import sync_to_async
from django.conf import settings
from mixpanel import Mixpanel

from backend.decorators import (
    require_login, require_project_access,
    enforce_group_level_auth_async
)
from backend.domain import resources, project as project_domain
from backend.typing import (
    Resource as ResourceType,
    Resources as ResourcesType,
    DownloadFilePayload as DownloadFilePayloadType,
    SimplePayload as SimplePayloadType,
)
from backend.exceptions import InvalidProject
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@sync_to_async
def _get_project_name(project_name: str) -> Dict[str, str]:
    """Get project_name."""
    return dict(project_name=project_name)


@sync_to_async
def _get_repositories(project_name: str) -> Dict[str, List[ResourceType]]:
    """Get repositories."""
    project_info = cast(Dict[str, List[ResourceType]],
                        project_domain.get_attributes(project_name,
                                                      ['repositories']))
    return dict(repositories=project_info.get('repositories', []))


@sync_to_async
def _get_environments(project_name: str) -> Dict[str, List[ResourceType]]:
    """Get environments."""
    project_info = cast(Dict[str, List[ResourceType]],
                        project_domain.get_attributes(project_name,
                                                      ['environments']))
    return dict(environments=project_info.get('environments', []))


@sync_to_async
def _get_files(project_name: str) -> Dict[str, List[ResourceType]]:
    """Get files."""
    project_info = cast(Dict[str, List[ResourceType]],
                        project_domain.get_attributes(project_name,
                                                      ['files']))
    return dict(files=project_info.get('files', []))


async def _resolve_fields(info, project_name: str) -> ResourcesType:
    """Async resolve fields."""
    result: ResourcesType = dict(
        repositories=list(),
        environments=list(),
        files=list()
    )
    tasks = list()
    project_name = project_name.lower()

    project_exist = project_domain.get_attributes(
        project_name, ['project_name']
    )
    if not project_exist:
        raise InvalidProject
    for requested_field in info.field_nodes[0].selection_set.selections:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'project_name': project_name
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        future = asyncio.ensure_future(
            resolver_func(**params)
        )
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)

    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_resources(_, info, project_name: str) -> ResourcesType:
    """Resolve resources query."""
    return util.run_async(_resolve_fields, info, project_name)


@convert_kwargs_to_snake_case
def resolve_resources_mutation(obj, info, **parameters):
    """Wrap resources mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_add_repositories(_, info, repos: List[Dict[str, str]],
                               project_name: str) -> SimplePayloadType:
    """Resolve add_repositories mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    new_repos = util.camel_case_list_dict(repos)
    success = await sync_to_async(resources.create_resource)(
        new_repos, project_name, 'repository', user_email)

    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Added repos to '
            f'{project_name} project succesfully')  # pragma: no cover
        await sync_to_async(resources.send_mail)(
            project_name, user_email, new_repos, 'added', 'repository')
    else:
        await sync_to_async(rollbar.report_message)(
            'An error occurred adding repositories',
            level='error',
            payload_data=locals())
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to add '
            f'repos to {project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_add_environments(_, info, envs: List[Dict[str, str]],
                               project_name: str) -> SimplePayloadType:
    """Resolve add_environments mutation."""
    new_envs = util.camel_case_list_dict(envs)
    user_email = util.get_jwt_content(info.context)['user_email']
    success = await sync_to_async(resources.create_resource)(
        new_envs, project_name, 'environment', user_email)

    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Added envs to '
            f'{project_name} project succesfully')  # pragma: no cover
        await sync_to_async(resources.send_mail)(
            project_name, user_email, new_envs, 'added', 'environment')
    else:
        await sync_to_async(rollbar.report_message)(
            'An error occurred adding environments',
            level='error',
            payload_data=locals())
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to add '
            f'envs to {project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_add_files(_, info, **parameters) -> SimplePayloadType:
    """Resolve add_files mutation."""
    success = False
    files_data = parameters['files_data']
    new_files_data = util.camel_case_list_dict(files_data)
    uploaded_file = parameters['file']
    project_name = parameters['project_name']
    user_email = util.get_jwt_content(info.context)['user_email']
    add_file = await sync_to_async(resources.create_file)(new_files_data,
                                                          uploaded_file,
                                                          project_name,
                                                          user_email)
    if add_file:
        await sync_to_async(resources.send_mail)(
            project_name, user_email, new_files_data, 'added', 'file')

        success = True
    else:
        await sync_to_async(rollbar.report_message)('Error: \
An error occurred uploading file', 'error', info.context)
    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Added resource files to \
            {project_name} project succesfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Attempted to add resource files \
from {project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_remove_files(_, info, files_data: Dict[str, Any],
                           project_name: str) -> SimplePayloadType:
    """Resolve remove_files mutation."""
    success = False
    files_data = {re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
                  for k, v in files_data.items()}
    file_name = files_data.get('fileName')
    user_email = util.get_jwt_content(info.context)['user_email']
    remove_file = await \
        sync_to_async(resources.remove_file)(file_name, project_name)
    if remove_file:
        await sync_to_async(resources.send_mail)(
            project_name, user_email, [files_data], 'removed', 'file')
        success = True
    else:
        await sync_to_async(rollbar.report_message)('Error: \
An error occurred removing file', 'error', info.context)
    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Removed Files from \
            {project_name} project succesfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to remove files \
from {project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_download_file(_, info, **parameters) -> DownloadFilePayloadType:
    """Resolve download_file mutation."""
    success = False
    file_info = parameters['files_data']
    project_name = parameters['project_name'].lower()
    user_email = util.get_jwt_content(info.context)['user_email']
    signed_url = await \
        sync_to_async(resources.download_file)(file_info, project_name)
    if signed_url:
        msg = 'Security: Downloaded file {file_name} in \
project {project} succesfully'\
            .format(project=project_name, file_name=parameters['files_data'])
        await sync_to_async(util.cloudwatch_log)(
            info.context, msg)  # pragma: no cover
        mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
        await sync_to_async(mp_obj.track)(user_email, 'DownloadProjectFile', {
            'Project': project_name.upper(),
            'Email': user_email,
            'FileName': parameters['files_data'],
        })
        success = True
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to download file {file_name} \
in project {project}'.format(
                project=project_name,
                file_name=parameters['files_data']))  # pragma: no cover
        await sync_to_async(rollbar.report_message)('Error: \
An error occurred generating signed URL', 'error', info.context)
    return DownloadFilePayloadType(success=success, url=str(signed_url))


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_update_environment(_, info, project_name: str,
                                 env: Dict[str, str],
                                 state: str) -> SimplePayloadType:
    """Resolve update_environment mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    env = {re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
           for k, v in env.items()}
    success = await sync_to_async(resources.update_resource)(
        env, project_name, 'environment', user_email)

    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Updated environment state in {project_name} '
            'project succesfully')  # pragma: no cover

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await sync_to_async(resources.send_mail)(
            project_name, user_email, [env], action, 'environment')
    else:
        await sync_to_async(rollbar.report_message)(
            'An error occurred updating environment state',
            level='error',
            payload_data=locals())
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to update environment state in '
            f'{project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_update_repository(_, info, project_name: str,
                                repo: Dict[str, str],
                                state: str) -> SimplePayloadType:
    """Resolve update_repository mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    repo = {re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
            for k, v in repo.items()}
    success = await sync_to_async(resources.update_resource)(
        repo, project_name, 'repository', user_email)

    if success:
        util.invalidate_cache(project_name)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Updated repository state in {project_name} '
            'project succesfully')  # pragma: no cover

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await sync_to_async(resources.send_mail)(
            project_name, user_email, [repo], action, 'repository')
    else:
        await sync_to_async(rollbar.report_message)(
            'An error occurred updating repository state',
            level='error',
            payload_data=locals())
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to update repository state in '
            f'{project_name} project')  # pragma: no cover
    return SimplePayloadType(success=success)
