# Standard libraries
from typing import (
    Any,
    Dict,
    List,
)

# Third-party libraries

# Local libraries
from backend.typing import (
    MailContent as MailContentType,
    Resource as ResourceType,
)
from group_access import domain as group_access_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_RESOURCERS,
)
from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


def _format_resource(
    resource_list: List[ResourceType],
    resource_type: str
) -> List[Dict[str, str]]:
    resource_description = []
    for resource_item in resource_list:
        resource_text = ''
        if resource_type == 'file':
            resource_text = str(resource_item.get('fileName', ''))
        resource_description.append({'resource_description': resource_text})
    return resource_description


async def send_mail_update_resource(  # pylint: disable=too-many-arguments
    context: Any,
    group_name: str,
    user_email: str,
    resource_list: List[ResourceType],
    action: str,
    resource_type: str
) -> None:
    group_loader = context.group_all
    group = await group_loader.load(group_name.lower())
    org_id = group['organization']

    organization_loader = context.organization
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    recipients = set(await group_access_domain.list_group_managers(group_name))
    recipients.add(user_email)
    recipients.update(FI_MAIL_RESOURCERS.split(','))
    mail_context: MailContentType = {
        'project': group_name.lower(),
        'organization': org_name,
        'user_email': user_email,
        'action': action,
        'resource_type': (
            f'{resource_type}s' if len(resource_list) > 1 else resource_type
        ),
        'resource_list': _format_resource(resource_list, resource_type),
        'project_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/resources'
        )
    }
    await send_mails_async_new(
        list(recipients),
        mail_context,
        GENERAL_TAG,
        f'Changes in resources for [{group_name}]',
        'resources_changes'
    )
