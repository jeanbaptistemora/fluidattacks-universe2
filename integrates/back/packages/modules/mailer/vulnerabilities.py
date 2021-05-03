# Standard libraries
from typing import (
    Any,
    Dict,
)

# Third-party libraries

# Local libraries
from backend.typing import Finding as FindingType
from group_access import domain as group_access_domain
from __init__ import BASE_URL
from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


async def send_mail_updated_treatment(
    context: Any,
    treatment: str,
    finding: Dict[str, FindingType],
    vulnerabilities: str
) -> None:
    finding_id = str(finding['finding_id'])
    group_name = str(finding['project_name'])

    group_loader = context.group_all
    group = await group_loader.load(group_name)
    org_id = group['organization']

    organization_loader = context.organization
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    managers = await group_access_domain.get_managers(group_name)
    email_context = {
        'project': group_name,
        'treatment': treatment,
        'finding': finding['title'],
        'vulnerabilities': vulnerabilities.splitlines(),
        'finding_link': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
            f'/vulns/{finding_id}'
        )
    }
    await send_mails_async_new(
        managers,
        email_context,
        GENERAL_TAG,
        (
            f'A vulnerability treatment has changed to '
            f'{email_context["treatment"]} in [{email_context["project"]}]'
        ),
        'updated_treatment'
    )
