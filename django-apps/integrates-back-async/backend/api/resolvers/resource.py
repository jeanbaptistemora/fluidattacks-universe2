# pylint: disable=import-error

from typing import Any, Dict, List as _List
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
from backend.exceptions import InvalidProject
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@sync_to_async
def _get_repositories(project_name: str):
    """Get repositories."""
    project_info = project_domain.get_attributes(
        project_name, ['repositories']
    )
    return dict(repositories=project_info.get('repositories', []))


@sync_to_async
def _get_environments(project_name: str):
    """Get environments."""
    project_info = project_domain.get_attributes(
        project_name, ['environments']
    )
    return dict(environments=project_info.get('environments', []))


@sync_to_async
def _get_files(project_name: str):
    """Get files."""
    project_info = project_domain.get_attributes(
        project_name, ['files']
    )
    return dict(files=project_info.get('files', []))


async def _resolve_fields(info, project_name):
    """Async resolve fields."""
    result = dict(
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
        snk_fld = convert_camel_case_to_snake(requested_field.name.value)
        if snk_fld.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snk_fld}'
        )
        future = asyncio.ensure_future(resolver_func(project_name))
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)

    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_resources(_, info, project_name):
    """Resolve resources query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields(info, project_name)
    )
    loop.close()
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_add_repositories(
    _, info, repos: _List[Dict[str, str]], project_name: str
) -> object:
    """Resolve add_repositories mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    success = resources.create_resource(
        repos, project_name, 'repository', user_email)

    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Added repos to {project_name} project succesfully')
        resources.send_mail(
            project_name, user_email, repos, 'added', 'repository')
    else:
        rollbar.report_message(
            'An error occurred adding repositories',
            level='error',
            payload_data=locals())
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add repos to {project_name} project')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_add_environments(
    _, info, envs: _List[Dict[str, str]], project_name: str
) -> object:
    """Resolve add_environments mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    success = resources.create_resource(
        envs, project_name, 'environment', user_email)

    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Added envs to {project_name} project succesfully')
        resources.send_mail(
            project_name, user_email, envs, 'added', 'environment')
    else:
        rollbar.report_message(
            'An error occurred adding environments',
            level='error',
            payload_data=locals())
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add envs to {project_name} project')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_add_files(_, info, **parameters):
    """Resolve add_files mutation."""
    success = False
    files_data = parameters['files_data']
    uploaded_file = parameters['file']
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
        util.cloudwatch_log(info.context, 'Security: Added resource files to \
            {project} project succesfully'.format(project=project_name))
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to add resource files \
from {project} project'.format(project=project_name))
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_remove_files(
    _, info, files_data: Dict[str, Any], project_name: str
) -> object:
    """Resolve remove_files mutation."""
    success = False
    file_name = files_data.get('file_name')
    user_email = util.get_jwt_content(info.context)['user_email']
    remove_file = resources.remove_file(file_name, project_name)
    if remove_file:
        resources.send_mail(project_name,
                            user_email,
                            [files_data],
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
        util.cloudwatch_log(
            info.context, 'Security: Attempted to remove files \
from {project} project'.format(project=project_name))
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_download_file(_, info, **parameters):
    """Resolve download_file mutation."""
    success = False
    file_info = parameters['files_data']
    project_name = parameters['project_name'].lower()
    user_email = util.get_jwt_content(info.context)['user_email']
    signed_url = resources.download_file(file_info, project_name)
    if signed_url:
        msg = 'Security: Downloaded file {file_name} in \
project {project} succesfully'\
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
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to download file {file_name} \
in project {project}'.format(project=project_name,
                             file_name=parameters['files_data']))
        rollbar.report_message('Error: \
An error occurred generating signed URL', 'error', info.context)
    return dict(success=success, url=str(signed_url))


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_update_environment(
    _, info, project_name: str, env: Dict[str, str], state: str
) -> object:
    """Resolve update_environment mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    env = {re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
           for k, v in env.items()}
    success = resources.update_resource(
        env, project_name, 'environment', user_email)

    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Updated environment state in {project_name} '
            'project succesfully')

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        resources.send_mail(
            project_name, user_email, [env], action, 'environment')
    else:
        rollbar.report_message(
            'An error occurred updating environment state',
            level='error',
            payload_data=locals())
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to update environment state in '
            f'{project_name} project')
    return dict(success=success)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_update_repository(
    _, info, project_name: str, repo: Dict[str, str], state: str
) -> object:
    """Resolve update_repository mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    repo = {re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
            for k, v in repo.items()}
    success = resources.update_resource(
        repo, project_name, 'repository', user_email)

    if success:
        util.invalidate_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Updated repository state in {project_name} '
            'project succesfully')

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        resources.send_mail(
            project_name, user_email, [repo], action, 'repository')
    else:
        rollbar.report_message(
            'An error occurred updating repository state',
            level='error',
            payload_data=locals())
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to update repository state in '
            f'{project_name} project')
    return dict(success=success)
