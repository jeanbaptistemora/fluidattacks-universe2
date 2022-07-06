from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    in_thread,
)
from context import (
    BASE_URL,
)
from db_model.enums import (
    Notification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access import (
    domain as group_access_domain,
)
import html
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from notifications import (
    dal as notifications_dal,
)
from typing import (
    Any,
    cast,
    Dict,
    Union,
)


async def _get_recipient_first_name_async(loaders: Any, email: str) -> str:
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    first_name = stakeholder.first_name
    if not first_name:
        first_name = email.split("@")[0]
    else:
        # First name exists in database
        pass
    return str(first_name)


async def cancel_health_check(
    requester_email: str, group_name: str, repo_url: str, branch: str
) -> None:
    await in_thread(
        notifications_dal.create_ticket,
        subject=f"[ASM] Health Check canceled: {group_name}",
        description=f"""
            You are receiving this email because you have canceled a health
            check for a repository through ASM by Fluid Attacks.

            Here are the details of the repository:
            - URL: {repo_url}
            - branch: {branch}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


async def delete_group(
    *,
    loaders: Any,
    deletion_date: str,
    group_name: str,
    requester_email: str,
    reason: str,
) -> bool:
    group: Group = await loaders.group.load(group_name)
    org_id = group.organization_id
    organization: Organization = await loaders.organization.load(org_id)
    org_name = organization.name
    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=f"[ASM] Group deleted: {group_name}",
            description=f"""
                You are receiving this email because you have deleted a group
                through ASM by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Deletion date: {deletion_date}
                - Deletion reason: {reason}
                - Organization name : {org_name}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
    )


async def update_group(  # pylint: disable=too-many-locals
    *,
    loaders: Any,
    comments: str,
    group_name: str,
    group_state: GroupState,
    had_asm: bool,
    has_asm: bool,
    has_machine: bool,
    has_squad: bool,
    reason: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    old_subscription: str = str(group_state.type.value).lower()
    old_service = group_state.service
    translations: dict[Any, str] = {
        "continuous": "Continuous Hacking",
        "oneshot": "One-Shot Hacking",
        True: "Active",
        False: "Inactive",
    }
    group_changes: dict[str, Any] = {
        "Name": group_name,
        "Type": {
            "from": translations.get(old_subscription, old_subscription),
            "to": translations.get(subscription, subscription),
        },
        "Service": {
            "from": str(old_service.value if old_service else "").capitalize(),
            "to": service.capitalize(),
        },
        "ASM": {
            "from": translations[had_asm],
            "to": translations[has_asm],
        },
        "Machine": {
            "from": translations[group_state.has_machine],
            "to": translations[has_machine],
        },
        "Squad": {
            "from": translations[group_state.has_squad],
            "to": translations[has_squad],
        },
        "Comments": html.escape(comments, quote=True),
        "Reason": reason.replace("_", " ").capitalize(),
    }

    description_body: str = ""

    for key, value in group_changes.items():
        description_body += f"- {key}: "
        description_body += (
            f"{value}\n"
            if key in ["Comments", "Reason", "Name"]
            else f"\n\tfrom: {value['from']}\n\tto: {value['to']}\n"
        )

    description: str = (
        "You are receiving this email because you have edited a group through "
        "ASM by Fluid Attacks. \n\nHere are the details of the group:"
        f"\n{description_body}\n\nIf you require any further information, "
        "do not hesitate to contact us."
    )

    await send_mail_services(
        loaders=loaders,
        group_name=group_name,
        group_changes=group_changes,
        requester_email=requester_email,
    )

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=f"[ASM] Group edited: {group_name}",
            description=description,
            requester_email=requester_email,
        ),
    )


async def send_mail_services(
    *,
    loaders: Any,
    group_name: str,
    group_changes: dict[str, Any],
    requester_email: str,
) -> None:
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    users_email = await group_access_domain.get_users_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=Notification.SERVICE_UPDATE,
        roles=roles,
    )

    await groups_mail.send_mail_updated_services(
        loaders=loaders,
        group_name=group_name,
        responsible=requester_email,
        group_changes=group_changes,
        report_date=datetime_utils.get_iso_date(),
        email_to=users_email,
    )


async def new_group(
    *,
    description: str,
    group_name: str,
    has_machine: bool,
    has_squad: bool,
    organization: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    translations: Dict[Union[str, bool], str] = {
        "continuous": "Continuous Hacking",
        "oneshot": "One-Shot Hacking",
        True: "Active",
        False: "Inactive",
    }

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=f"[ASM] Group created: {group_name}",
            description=f"""
                You are receiving this email because you have created a group
                through ASM by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Description: {description}
                - Type: {translations.get(subscription, subscription)}
                - Service: {service}
                - Organization: {organization}
                - Squad: {translations[has_squad]}
                - Machine: {translations[has_machine]}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
    )


async def managed_manually(
    *,
    group_name: str,
    managed: GroupManaged,
    organization_name: str,
    requester_email: str,
) -> bool:
    translations: Dict[str, str] = {
        "MANUALLY": "Manually",
        "NOT_MANUALLY": "Not Manually",
        "UNDER_REVIEW": "Under Review",
    }

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=(
                f"[ASM] {translations[managed]} managed requested:"
                f" {group_name}"
            ),
            description=f"""
                You are receiving this email because you have requested
                to {translations[managed]} managed a group, through ASM
                by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Organization: {organization_name}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
    )


async def new_password_protected_report(
    loaders: Any,
    user_email: str,
    group_name: str,
    file_type: str,
    file_link: str = "",
) -> None:
    today = datetime_utils.get_now()
    fname = await _get_recipient_first_name_async(loaders, user_email)
    subject = f"{file_type} Report for [{group_name}]"
    await groups_mail.send_mail_group_report(
        [user_email],
        {
            "filetype": file_type,
            "fname": fname,
            "date": datetime_utils.get_as_str(today, "%Y-%m-%d"),
            "year": datetime_utils.get_as_str(today, "%Y"),
            "time": datetime_utils.get_as_str(today, "%H:%M"),
            "groupname": group_name,
            "subject": subject,
            "filelink": file_link,
        },
    )


async def request_health_check(
    requester_email: str, group_name: str, repo_url: str, branch: str
) -> None:
    await in_thread(
        notifications_dal.create_ticket,
        subject=f"[ASM] Health Check requested: {group_name}",
        description=f"""
            You are receiving this email because you have requested a health
            check for a repository in {group_name.capitalize()} group
            through ASM by Fluid Attacks.

            Here are the details of the repository:
            - URL: {repo_url}
            - branch: {branch}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


async def request_vulnerability_zero_risk(
    loaders: Any,
    finding_id: str,
    justification: str,
    requester_email: str,
) -> bool:
    finding_loader: DataLoader = loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    finding_title = finding.title
    group_name = finding.group_name

    group: Group = await loaders.group.load(group_name)
    org_id = group.organization_id
    organization: Organization = await loaders.organization.load(org_id)
    org_name = organization.name
    finding_url = (
        f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/vulns/"
        f"{finding_id}/locations"
    )
    description = f"""
        You are receiving this case because a zero risk vulnerability has been
        requested through ASM by Fluid Attacks.

        Here are the details of the zero risk vulnerability:
        Group: {group_name}

        - Finding: {finding_title}
        - ID: {finding_id}
        - URL: {finding_url}
        - Justification: {justification}

        If you require any further information,
        do not hesitate to contact us.
    """

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject="[ASM] Requested zero risk vulnerabilities",
            description=description,
            requester_email=requester_email,
        ),
    )


async def request_groups_upgrade(
    loaders: Any,
    user_email: str,
    groups: tuple[Group, ...],
) -> None:
    organization_ids = set(group.organization_id for group in groups)
    organizations: tuple[Organization] = await loaders.organization.load_many(
        organization_ids
    )

    organizations_message = "".join(
        f"""
            - Organization {organization.name}:
                {', '.join(
                    group.name
                    for group in groups
                    if group.organization_id == organization.id)
                }
        """
        for organization in organizations
    )

    await in_thread(
        notifications_dal.create_ticket,
        subject="[ASM] Subscription upgrade requested",
        description=f"""
            You are receiving this email because you have requested an upgrade
            to the Squad plan for the following groups:
            {organizations_message}
            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=user_email,
    )
