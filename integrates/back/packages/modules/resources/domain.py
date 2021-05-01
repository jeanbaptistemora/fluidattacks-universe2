"""Domain functions for resources."""

# Standard libraries
import logging
import logging.config
from typing import (
    Any,
    cast,
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    schedule,
)
from starlette.datastructures import UploadFile

# Local libraries
from back.settings import (
    LOGGING,
    NOEXTRA
)
from backend import util
from backend.typing import (
    MailContent as MailContentType,
    Resource as ResourceType
)
from custom_exceptions import InvalidFileSize
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from mailer import resources as resources_mail
from newutils import (
    datetime as datetime_utils,
    resources as resources_utils,
    validations,
)
from resources import dal as resources_dal
from __init__ import (
    BASE_URL,
    FI_MAIL_RESOURCERS,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def create_file(
    files_data: List[Dict[str, str]],
    uploaded_file: UploadFile,
    project_name: str,
    user_email: str
) -> bool:
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
    file_id = f'{project_name}/{uploaded_file.filename}'
    try:
        file_size = 100
        await validate_file_size(uploaded_file, file_size)
    except InvalidFileSize as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    files = await groups_domain.get_attributes(project_name, ['files'])
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
            resources_utils.save_file(uploaded_file, file_id),
            groups_domain.update(project_name, {'files': project_files})
        ]))
    return success


def format_resource(
    resource_list: List[ResourceType],
    resource_type: str
) -> List[Dict[str, str]]:
    resource_description = []
    for resource_item in resource_list:
        if resource_type == 'file':
            resource_text = str(resource_item.get('fileName', ''))
        resource_description.append({'resource_description': resource_text})
    return resource_description


async def remove_file(file_name: str, project_name: str) -> bool:
    success = False
    project_name = project_name.lower()
    project = await groups_domain.get_attributes(project_name, ['files'])
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
            resources_utils.remove_file(file_url),
            resources_dal.remove(project_name, 'files', index)
        ]))
    return success


async def send_mail(  # pylint: disable=too-many-arguments
    context: Any,
    group_name: str,
    user_email: str,
    resource_list: List[ResourceType],
    action: str,
    resource_type: str
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    recipients = set(await group_access_domain.list_group_managers(group_name))
    recipients.add(user_email)
    recipients.update(FI_MAIL_RESOURCERS.split(','))
    resource_description = format_resource(resource_list, resource_type)

    group = await group_loader.load(group_name.lower())
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    if len(resource_list) > 1:
        resource_type = f'{resource_type}s'
    else:
        # resource_type is the same
        pass
    mail_context: MailContentType = {
        'project': group_name.lower(),
        'organization': org_name,
        'user_email': user_email,
        'action': action,
        'resource_type': resource_type,
        'resource_list': resource_description,
        'project_url': f'{BASE_URL}/orgs/{org_name}/groups/'
                       f'{group_name}/resources'
    }
    schedule(
        resources_mail.send_mail_resources(list(recipients), mail_context)
    )


async def validate_file_size(
    uploaded_file: UploadFile,
    file_size: int
) -> bool:
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    if await util.get_file_size(uploaded_file) > file_size * mib:
        raise InvalidFileSize()
    return True
