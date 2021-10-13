from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from group_access import (
    domain as group_access_domain,
)
from typing import (
    Any,
)


async def send_mail_updated_treatment(
    *,
    loaders: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    treatment: str,
    vulnerabilities: str,
) -> None:
    group_loader = loaders.group
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization["name"]

    managers = await group_access_domain.get_managers(group_name)
    email_context = {
        "group": group_name,
        "treatment": treatment,
        "finding": finding_title,
        "vulnerabilities": vulnerabilities.splitlines(),
        "finding_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}"
        ),
    }
    await send_mails_async(
        managers,
        email_context,
        GENERAL_TAG,
        (
            f"A vulnerability treatment has changed to "
            f'{email_context["treatment"]} in [{email_context["group"]}]'
        ),
        "updated_treatment",
    )
