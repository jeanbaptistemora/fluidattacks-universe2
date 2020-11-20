import logging
import re
import sys
from typing import Any, Dict, List, cast, Union

from aioextensions import (
    in_thread,
)
from ariadne import convert_kwargs_to_snake_case
from mixpanel import Mixpanel
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    concurrent_decorators,
    require_login,
    require_integrates,
    enforce_group_level_auth_async
)
from backend.domain import resources
from backend.typing import (
    Resource as ResourceType,
    DownloadFilePayload as DownloadFilePayloadType,
    SimplePayload as SimplePayloadType,
)
from backend.utils import virus_scan
from backend import util

from backend_new import settings

from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def _clean_resources_cache(project_name: str) -> None:
    util.queue_cache_invalidation(
        # resource entity related
        f'environments*{project_name}',
        f'files*{project_name}',
        f'repositories*{project_name}',
        # project entity related
        f'has*{project_name}',
        f'deletion*{project_name}',
        f'tags*{project_name}',
        f'subscription*{project_name}',
    )


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_resources_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[SimplePayloadType, DownloadFilePayloadType]:
    """Wrap resources mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[SimplePayloadType, DownloadFilePayloadType],
        await resolver_func(obj, info, **parameters)
    )


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_repositories(
        _: Any,
        info: GraphQLResolveInfo,
        repos: List[Dict[str, str]],
        project_name: str) -> SimplePayloadType:
    """Resolve add_repositories mutation."""
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    new_repos = util.camel_case_list_dict(repos)
    success = await resources.create_repositories(
        new_repos, project_name, user_email
    )

    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Added repos to '
             f'{project_name} project successfully')  # pragma: no cover
        )
        await resources.send_mail(
            project_name,
            user_email,
            new_repos,
            'added',
            'repository'
        )
    else:
        LOGGER.error('Couldn\'t add repositories', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to add '
             f'repos to {project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_environments(
        _: Any,
        info: GraphQLResolveInfo,
        envs: List[Dict[str, str]],
        project_name: str) -> SimplePayloadType:
    """Resolve add_environments mutation."""
    new_envs = util.camel_case_list_dict(envs)
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    success = await resources.create_environments(
        new_envs, project_name, user_email
    )

    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Added envs to '
             f'{project_name} project successfully')  # pragma: no cover
        )
        await resources.send_mail(
            project_name,
            user_email,
            new_envs,
            'added',
            'environment'
        )
    else:
        LOGGER.error('Couldn\'t add environments', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to add '
             f'envs to {project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_files(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> SimplePayloadType:
    """Resolve add_files mutation."""
    success = False
    files_data = parameters['files_data']
    new_files_data = util.camel_case_list_dict(files_data)
    uploaded_file = parameters['file']
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    project_name = parameters['project_name']

    virus_scan.scan_file(uploaded_file, user_email, project_name)

    add_file = await resources.create_file(
        new_files_data,
        uploaded_file,
        project_name,
        user_email
    )
    if add_file:
        await resources.send_mail(
            project_name,
            user_email,
            new_files_data,
            'added',
            'file'
        )

        success = True
    else:
        LOGGER.error('Couldn\'t upload file', extra={'extra': parameters})
    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Added resource files to '
             f'{project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to add resource files '
             f'from {project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_remove_files(
        _: Any,
        info: GraphQLResolveInfo,
        files_data: Dict[str, Any],
        project_name: str) -> SimplePayloadType:
    """Resolve remove_files mutation."""
    success = False
    files_data = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in files_data.items()
    }
    file_name = files_data.get('fileName')
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    remove_file = await resources.remove_file(str(file_name), project_name)
    if remove_file:
        await resources.send_mail(
            project_name,
            user_email,
            [files_data],
            'removed',
            'file'
        )
        success = True
    else:
        LOGGER.error(
            'Couldn\'t remove file',
            extra={
                'extra': {
                    'file_name': file_name,
                    'project_name': project_name,
                }
            })
    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Removed Files from '
             f'{project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to remove files '
             f'from {project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_download_file(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> DownloadFilePayloadType:
    """Resolve download_file mutation."""
    success = False
    file_info = parameters['files_data']
    project_name = parameters['project_name'].lower()
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    signed_url = await resources.download_file(
        file_info, project_name
    )
    if signed_url:
        msg = (
            f'Security: Downloaded file {parameters["files_data"]} '
            f'in project {project_name} successfully'
        )
        util.cloudwatch_log(info.context, msg)  # pragma: no cover
        mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
        await in_thread(
            mp_obj.track,
            user_email,
            'DownloadProjectFile',
            {
                'Project': project_name.upper(),
                'Email': user_email,
                'FileName': parameters['files_data'],
            }
        )
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to download file '
             f'{parameters["files_data"]}'
             f' in project {project_name}')  # pragma: no cover
        )
        LOGGER.error(
            'Couldn\'t generate signed URL',
            extra={'extra': parameters})
    return DownloadFilePayloadType(success=success, url=str(signed_url))


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_update_environment(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        env: Dict[str, str],
        state: str) -> SimplePayloadType:
    """Resolve update_environment mutation."""
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    env = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in env.items()
    }
    success = await resources.update_resource(
        cast(ResourceType, env),
        project_name,
        'environment',
        user_email
    )

    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            (f'Security: Updated environment state in {project_name} '
             'project successfully')  # pragma: no cover
        )

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await resources.send_mail(
            project_name,
            user_email,
            cast(List[ResourceType], [env]),
            action,
            'environment'
        )
    else:
        LOGGER.error(
            'Couldn\'t update environment state', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update environment state in '
             f'{project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_update_repository(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        repo: Dict[str, str],
        state: str) -> SimplePayloadType:
    """Resolve update_repository mutation."""
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    repo = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in repo.items()
    }
    success = await resources.update_resource(
        cast(ResourceType, repo),
        project_name,
        'repository',
        user_email
    )

    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            (f'Security: Updated repository state in {project_name} '
             'project successfully')  # pragma: no cover
        )

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await resources.send_mail(
            project_name,
            user_email,
            cast(List[ResourceType], [repo]),
            action,
            'repository'
        )
    else:
        LOGGER.error(
            'Couldn\'t update repository state', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update repository state in '
             f'{project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
