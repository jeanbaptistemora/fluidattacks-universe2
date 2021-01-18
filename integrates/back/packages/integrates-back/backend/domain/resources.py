"""Domain functions for resources."""

import logging
from collections import namedtuple
from typing import Dict, List, NamedTuple, cast

from aioextensions import (
    collect,
    schedule,
)
from starlette.datastructures import UploadFile

from backend import mailer
from backend import util
from backend.dal import (
    project as project_dal,
    resources as resources_dal
)
from backend.typing import (
    MailContent as MailContentType,
    Resource as ResourceType
)
from backend.domain import (
    organization as org_domain
)
from backend.exceptions import InvalidFileSize
from backend.utils import (
    datetime as datetime_utils,
    validations,
)

from back.settings import (
    LOGGING,
    NOEXTRA
)

from __init__ import BASE_URL, FI_MAIL_RESOURCERS

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def format_resource(resource_list: List[ResourceType], resource_type: str) -> \
        List[Dict[str, str]]:
    resource_description = []
    for resource_item in resource_list:
        if resource_type == 'file':
            resource_text = str(resource_item.get('fileName', ''))
        resource_description.append({'resource_description': resource_text})
    return resource_description


async def send_mail(
        project_name: str,
        user_email: str,
        resource_list: List[ResourceType],
        action: str,
        resource_type: str) -> None:
    recipients = set(await project_dal.list_project_managers(project_name))
    recipients.add(user_email)
    recipients.update(FI_MAIL_RESOURCERS.split(','))
    resource_description = format_resource(resource_list, resource_type)
    org_id = await org_domain.get_id_for_group(project_name)
    org_name = await org_domain.get_name_by_id(org_id)
    if len(resource_list) > 1:
        resource_type = '{}s'.format(resource_type)
    else:
        # resource_type is the same
        pass
    context: MailContentType = {
        'project': project_name.lower(),
        'organization': org_name,
        'user_email': user_email,
        'action': action,
        'resource_type': resource_type,
        'resource_list': resource_description,
        'project_url': f'{BASE_URL}/orgs/{org_name}/groups/'
                       f'{project_name}/resources'
    }
    schedule(
        mailer.send_mail_resources(
            list(recipients), context
        )
    )


async def validate_file_size(
        uploaded_file: UploadFile,
        file_size: int) -> bool:
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    if await util.get_file_size(uploaded_file) > file_size * mib:
        raise InvalidFileSize()
    return True


async def create_file(
        files_data: List[Dict[str, str]],
        uploaded_file: UploadFile,
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
            'uploadDate': datetime_utils.get_as_str(
                datetime_utils.get_now(),
                date_format='%Y-%m-%d %H:%M'
            ),
            'uploader': user_email,
        })
    file_id = '{project}/{file_name}'.format(
        project=project_name,
        file_name=uploaded_file.filename
    )
    try:
        file_size = 100
        await validate_file_size(uploaded_file, file_size)
    except InvalidFileSize as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    files = await project_dal.get_attributes(project_name, ['files'])
    project_files = cast(List[ResourceType], files.get('files', []))
    if project_files:
        contains_repeated = [
            f.get('fileName')
            for f in project_files
            if f.get('fileName') == uploaded_file.filename
        ]
        if contains_repeated:
            LOGGER.error('File already exists', **NOEXTRA)
    else:
        # Project doesn't have files
        pass
    if validations.validate_file_name(uploaded_file.filename):
        project_files.extend(json_data)
        success = all(await collect([
            resources_dal.save_file(uploaded_file, file_id),
            project_dal.update(project_name, {'files': project_files})
        ]))

    return success


async def remove_file(file_name: str, project_name: str) -> bool:
    success = False
    project_name = project_name.lower()
    project = await project_dal.get_attributes(project_name, ['files'])
    file_list = cast(
        List[Dict[str, str]],
        project.get('files', [])
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
        success = all(await collect([
            resources_dal.remove_file(file_url),
            resources_dal.remove(project_name, 'files', index)
        ]))
    return success


async def download_file(file_info: str, project_name: str) -> str:
    return await resources_dal.download_file(file_info, project_name)


async def mask(project_name: str) -> NamedTuple:
    project_name = project_name.lower()
    project = await project_dal.get_attributes(
        project_name,
        ['environments', 'files', 'repositories']
    )
    Status: NamedTuple = namedtuple(
        'Status',
        ('are_files_removed files_result '
         'environments_result repositories_result')
    )
    list_resources_files = await resources_dal.search_file(f'{project_name}/')
    are_files_removed = all(await collect(
        resources_dal.remove_file(file_name)
        for file_name in list_resources_files
    ))

    files_result = await project_dal.update(project_name, {
        'files': [
            {
                'fileName': 'Masked',
                'description': 'Masked',
                'uploader': 'Masked'
            }
            for _ in project.get('files', [])
        ]
    })
    environments_result = await project_dal.update(project_name, {
        'environments': [
            {'urlEnv': 'Masked'}
            for _ in project.get('environments', [])
        ]
    })
    repositories_result = await project_dal.update(project_name, {
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
