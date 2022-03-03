from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from custom_types import (
    MailContent as MailContentType,
)
from db_model.enums import (
    Notification,
)
from db_model.users.get import (
    User,
)
from group_access import (
    domain as group_access_domain,
)
from mailer.utils import (
    get_organization_name,
)
from typing import (
    Any,
    List,
    Tuple,
)


async def send_mail_updated_treatment(  # pylint: disable=too-many-locals
    *,
    loaders: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    treatment: str,
    vulnerabilities: str,
    modified_by: str,
) -> None:
    group_loader = loaders.group
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization["name"]

    managers = await group_access_domain.get_managers(group_name)
    users: Tuple[User, ...] = await loaders.user.load_many(managers)
    users_email = [
        user.email
        for user in users
        if Notification.UPDATED_TREATMENT
        in user.notifications_preferences.email
    ]
    email_context = {
        "group": group_name,
        "responsible": modified_by,
        "treatment": treatment,
        "finding": finding_title,
        "vulnerabilities": vulnerabilities.splitlines(),
        "finding_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}"
        ),
    }
    await send_mails_async(
        users_email,
        email_context,
        GENERAL_TAG,
        (
            f"A vulnerability treatment has changed to "
            f'{email_context["treatment"]} in [{email_context["group"]}]'
        ),
        "updated_treatment",
    )


async def send_mail_assigned_vulnerability(
    *,
    loaders: Any,
    email_to: List[str],
    is_finding_released: bool,
    group_name: str = "",
    finding_title: str,
    finding_id: str,
    where: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)

    email_context: MailContentType = {
        "finding_title": finding_title,
        "group": group_name,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/"
            f'{"vulns" if is_finding_released else "drafts"}/{finding_id}/'
            "locations"
        ),
        "where": where.splitlines(),
    }
    await send_mails_async(
        email_to=email_to,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            "Newly assigned vulnerability in "
            f"[{finding_title}] for [{group_name}]"
        ),
        template_name="vulnerability_assigned",
    )
