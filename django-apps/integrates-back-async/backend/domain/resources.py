"""Domain functions for resources."""


from collections import namedtuple
from datetime import datetime
from urllib.parse import quote, unquote
from typing import Dict, List, NamedTuple, cast
import threading
from asgiref.sync import async_to_sync
import rollbar

from backend import mailer
from backend import util
from backend.dal import (
    project as project_dal,
    resources as resources_dal
)
from backend.typing import Resource as ResourceType
from backend.exceptions import (
    InvalidFileSize,
    RepeatedValues,
    InvalidResource
)
from backend.utils import validations, aio

from __init__ import BASE_URL, FI_MAIL_RESOURCERS


def format_resource(resource_list: List[ResourceType], resource_type: str) -> \
        List[Dict[str, str]]:
    resource_description = []
    for resource_item in resource_list:
        if resource_type == 'repository':
            repo_url = resource_item.get('urlRepo')
            repo_branch = resource_item.get('branch')
            resource_text = f'Repository: {repo_url} Branch: {repo_branch}'
        elif resource_type == 'environment':
            resource_text = str(resource_item.get('urlEnv', ''))
        elif resource_type == 'file':
            resource_text = str(resource_item.get('fileName', ''))
        resource_description.append({'resource_description': resource_text})
    return resource_description


def send_mail(
        project_name: str,
        user_email: str,
        resource_list: List[ResourceType],
        action: str,
        resource_type: str):
    recipients = set(project_dal.list_project_managers(project_name))
    recipients.add(user_email)
    recipients.update(FI_MAIL_RESOURCERS.split(','))
    resource_description = format_resource(resource_list, resource_type)
    if resource_type == 'repository' and len(resource_list) > 1:
        resource_type = 'repositories'
    elif len(resource_list) > 1:
        resource_type = '{}s'.format(resource_type)
    else:
        # resource_type is the same
        pass
    context = {
        'project': project_name.lower(),
        'user_email': user_email,
        'action': action,
        'resource_type': resource_type,
        'resource_list': resource_description,
        'project_url': f'{BASE_URL}/groups/{project_name}/resources'
    }
    threading.Thread(
        name='Remove repositories email thread',
        target=mailer.send_mail_resources,
        args=(list(recipients), context,)
    ).start()


def validate_file_size(uploaded_file, file_size: int) -> bool:
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    if uploaded_file.size > file_size * mib:
        raise InvalidFileSize()
    return True


async def create_file(
        files_data: List[Dict[str, str]],
        uploaded_file,
        project_name: str,
        user_email: str) -> bool:
    success = False
    project_name = project_name.lower()
    json_data: List[ResourceType] = []
    for file_info in files_data:
        description = file_info['description']
        validations.validate_fields(cast(List[str], [description]))
        validations.validate_field_length(description, 200)
        json_data.append({
            'fileName': file_info.get('fileName', file_info['fileName']),
            'description': description,
            'uploadDate': str(
                datetime.now().replace(second=0, microsecond=0)
            )[:-3],
            'uploader': user_email,
        })
    file_id = '{project}/{file_name}'.format(
        project=project_name,
        file_name=uploaded_file
    )
    try:
        file_size = 100
        validate_file_size(uploaded_file, file_size)
    except InvalidFileSize:
        rollbar.report_message('Error: File exceeds size limit', 'error')
    files = await project_dal.get_attributes(project_name, ['files'])
    project_files = cast(List[ResourceType], files.get('files', []))
    if project_files:
        contains_repeated = [
            f.get('fileName')
            for f in project_files
            if f.get('fileName') == uploaded_file.name
        ]
        if contains_repeated:
            rollbar.report_message('Error: File already exists', 'error')
    else:
        # Project doesn't have files
        pass
    if validations.validate_file_name(uploaded_file):
        project_files.extend(json_data)
        success = all(await aio.materialize([
            resources_dal.save_file(uploaded_file, file_id),
            project_dal.update(project_name, {'files': project_files})
        ]))

    return success


async def remove_file(file_name: str, project_name: str) -> bool:
    success = False
    project_name = project_name.lower()
    file_list = cast(
        List[Dict[str, str]],
        project_dal.get(project_name)['files']
    )
    index = -1
    cont = 0
    while index < 0 and len(file_list) > cont:
        if file_list[cont]['fileName'] == file_name:
            index = cont
        else:
            index = -1
        cont += 1
    if index >= 0:
        file_url = f'{project_name.lower()}/{file_name}'
        success = all(await aio.materialize([
            resources_dal.remove_file(file_url),
            resources_dal.remove(project_name, 'files', index)
        ]))
    return success


def download_file(file_info: str, project_name: str) -> str:
    return resources_dal.download_file(file_info, project_name)


def has_repeated_envs(
        existing_envs: List[ResourceType],
        envs: List[ResourceType]) -> bool:
    unique_inputs = list(
        {env['urlEnv']: env for env in envs}.values()
    )
    has_repeated_inputs = len(envs) != len(unique_inputs)

    all_envs = [{'urlEnv': env['urlEnv']} for env in existing_envs] + envs

    unique_envs = list(
        {env['urlEnv']: env for env in all_envs}.values()
    )
    has_repeated_existing = len(all_envs) != len(unique_envs)

    return has_repeated_inputs or has_repeated_existing


def has_repeated_repos(
        existing_repos: List[ResourceType],
        repos: List[ResourceType]) -> bool:
    unique_inputs = list({
        (repo['urlRepo'], repo['branch'], repo.get('protocol', '')): repo
        for repo in repos
    }.values())
    has_repeated_inputs = len(repos) != len(unique_inputs)

    all_repos = [
        {
            'urlRepo': repo['urlRepo'],
            'branch': repo['branch'],
            'protocol': repo.get('protocol', '')
        }
        for repo in existing_repos
    ] + repos

    unique_repos = list({
        (repo['urlRepo'], repo['branch'], repo.get('protocol')): repo
        for repo in all_repos
    }.values())
    has_repeated_existing = len(all_repos) != len(unique_repos)

    return has_repeated_inputs or has_repeated_existing


def encode_resources(res_data: List[Dict[str, str]]) -> List[ResourceType]:
    return [
        {
            key: quote(value, safe='')
            for key, value in res.items()
        } for res in res_data
    ]


def create_initial_state(user_email: str) -> Dict[str, str]:
    return {
        'user': user_email,
        'date': util.format_comment_date(
            datetime.today().strftime('%Y-%m-%d %H:%M:%S')),
        'state': 'ACTIVE'
    }


async def create_repositories(
        res_data: List[Dict[str, str]],
        project_name: str,
        user_email: str) -> bool:

    project_name = project_name.lower()

    repositories = await project_dal.get_attributes(
        project_name.lower(), ['repositories']
    )
    existing_repos = cast(
        List[ResourceType], repositories.get('repositories', [])
    )

    res_data_enc = encode_resources(res_data)
    if has_repeated_repos(existing_repos, res_data_enc):
        raise RepeatedValues()

    json_data: List[ResourceType] = []
    for res in res_data_enc:
        url_repo = str(res.get('urlRepo', ''))
        branch = str(res.get('branch', ''))
        validations.validate_field_length(url_repo, 300)
        validations.validate_field_length(branch, 30)
        res_object: ResourceType = {
            'urlRepo': url_repo,
            'branch': branch,
            'protocol': res.get('protocol', 'HTTPS'),
            'uploadDate': str(
                datetime.now().replace(second=0, microsecond=0))[:-3],
            'historic_state': [create_initial_state(user_email)],
        }
        json_data.append(res_object)

    existing_repos.extend(json_data)

    return await project_dal.update(
        project_name, {'repositories': existing_repos}
    )


async def create_environments(
        res_data: List[Dict[str, str]],
        project_name: str,
        user_email: str) -> bool:

    project_name = project_name.lower()

    res_data_enc = encode_resources(res_data)
    environments = await project_dal.get_attributes(
        project_name.lower(), ['environments']
    )
    existing_envs = cast(
        List[ResourceType], environments.get('environments', [])
    )
    if has_repeated_envs(existing_envs, res_data_enc):
        raise RepeatedValues()

    json_data: List[ResourceType] = []
    for res in res_data_enc:
        url_env = str(res.get('urlEnv', ''))
        validations.validate_field_length(url_env, 400)
        res_object = {
            'urlEnv': url_env,
            'historic_state': [create_initial_state(user_email)],
        }
        json_data.append(res_object)
    existing_envs.extend(json_data)

    return await project_dal.update(
        project_name, {'environments': existing_envs}
    )


async def update_resource(
        res_data: ResourceType,
        project_name: str,
        res_type: str,
        user_email: str) -> bool:
    res_list: List[ResourceType] = []
    project_info = await project_dal.get_attributes(
        project_name.lower(), ['environments', 'repositories']
    )

    if res_type == 'repository':
        res_list = cast(
            List[ResourceType],
            project_info.get('repositories', [])
        )
        res_id = 'urlRepo'
        res_name = 'repositories'
    elif res_type == 'environment':
        res_list = cast(
            List[ResourceType],
            project_info.get('environments', [])
        )
        res_id = 'urlEnv'
        res_name = 'environments'

    resource_exists = False
    for resource in res_list:
        if res_type == 'repository':
            matches = (
                unquote(cast(str, resource['branch'])),
                resource.get('protocol', ''),
                unquote(cast(str, resource['urlRepo']))
            ) == tuple(res_data.values())
        elif res_type == 'environment':
            src_url_env = unquote(cast(str, resource['urlEnv']))
            matches = src_url_env == res_data['urlEnv']

        if res_id in resource and matches:
            resource_exists = True
            new_state = {
                'user': user_email,
                'date': util.format_comment_date(
                    datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                ),
                'state': 'INACTIVE'
            }
            if 'historic_state' in resource:
                historic_state = cast(
                    List[Dict[str, str]],
                    resource['historic_state']
                )
                if not historic_state[-1]['state'] == 'ACTIVE':
                    new_state['state'] = 'ACTIVE'
                historic_state.append(new_state)
            else:
                historic_state = [new_state]
            resource['historic_state'] = historic_state
            break

    if not resource_exists:
        raise InvalidResource()

    return await project_dal.update(
        project_name.lower(), {res_name: res_list}
    )


def mask(project_name: str) -> NamedTuple:
    project_name = project_name.lower()
    project = async_to_sync(project_dal.get_attributes)(
        project_name,
        ['environments', 'files', 'repositories']
    )
    Status: NamedTuple = namedtuple(
        'Status',
        ('are_files_removed files_result '
         'environments_result repositories_result')
    )
    are_files_removed = all([
        async_to_sync(resources_dal.remove_file)(file_name)
        for file_name in resources_dal.search_file(f'{project_name}/')
    ])
    files_result = async_to_sync(project_dal.update)(project_name, {
        'files': [
            {
                'fileName': 'Masked',
                'description': 'Masked',
                'uploader': 'Masked'
            }
            for _ in project.get('files', [])
        ]
    })
    environments_result = async_to_sync(project_dal.update)(project_name, {
        'environments': [
            {'urlEnv': 'Masked'}
            for _ in project.get('environments', [])
        ]
    })
    repositories_result = async_to_sync(project_dal.update)(project_name, {
        'repositories': [
            {'protocol': 'Masked', 'urlRepo': 'Masked'}
            for _ in project.get('repositories', [])
        ]
    })
    success = cast(
        NamedTuple,
        Status(
            are_files_removed,
            files_result,
            environments_result,
            repositories_result
        )
    )
    return success
