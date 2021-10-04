from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_thread,
)
from context import (
    BASE_URL,
    FI_API_STATUS,
)
from custom_types import (
    Finding as FindingType,
)
from db_model.findings.types import (
    Finding,
)
from exponent_server_sdk import (
    DeviceNotRegisteredError,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import html
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from notifications import (
    dal as notifications_dal,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    cast,
    Dict,
    List,
    Union,
)
from users import (
    domain as users_domain,
)


async def _get_recipient_first_name_async(email: str) -> str:
    first_name = await users_domain.get_data(email, "first_name")
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
    deletion_date: str,
    group_name: str,
    requester_email: str,
    reason: str,
) -> bool:
    org_id = await orgs_domain.get_id_for_group(group_name)
    org_name = await orgs_domain.get_name_by_id(org_id)
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


async def update_group(
    *,
    comments: str,
    group_name: str,
    had_machine: bool,
    had_squad: bool,
    had_asm: bool,
    has_machine: bool,
    has_squad: bool,
    has_asm: bool,
    reason: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    # pylint: disable=unsubscriptable-object
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
            subject=f"[ASM] Group edited: {group_name}",
            description=f"""
                You are receiving this email because you have edited a group
                through ASM by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Type: {translations.get(subscription, subscription)}
                - Service: {service.capitalize()}
                - ASM:
                    from: {translations[had_asm]}
                    to: {translations[has_asm]}
                - Machine:
                    from: {translations[had_machine]}
                    to: {translations[has_machine]}
                - Squad:
                    from: {translations[had_squad]}
                    to: {translations[has_squad]}
                - Comments: {html.escape(comments, quote=True)}
                - Reason: {reason}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
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
    # pylint: disable=unsubscriptable-object
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


async def new_password_protected_report(
    user_email: str,
    group_name: str,
    passphrase: str,
    file_type: str,
    file_link: str = "",
) -> None:
    today = datetime_utils.get_now()
    fname = await _get_recipient_first_name_async(user_email)
    subject = f"{file_type} Report for [{group_name}]"
    await collect(
        (
            send_push_notification(
                user_email, f"{file_type} report passphrase", passphrase
            ),
            groups_mail.send_mail_group_report(
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
            ),
        )
    )


async def request_health_check(
    requester_email: str, group_name: str, repo_url: str, branch: str
) -> None:
    await in_thread(
        notifications_dal.create_ticket,
        subject=f"[ASM] Health Check requested: {group_name}",
        description=f"""
            You are receiving this email because you have requested a health
            check for a repository through ASM by Fluid Attacks.

            Here are the details of the repository:
            - URL: {repo_url}
            - branch: {branch}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


async def request_vulnerability_zero_risk(
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    requester_email: str,
) -> bool:
    if FI_API_STATUS == "migration":
        finding_new_loader: DataLoader = info.context.loaders.finding_new
        finding_new: Finding = await finding_new_loader.load(finding_id)
        finding_title = finding_new.title
        finding_type = ""
        group_name = finding_new.group_name
    else:
        finding_loader: DataLoader = info.context.loaders.finding
        finding: Dict[str, FindingType] = await finding_loader.load(finding_id)
        finding_title = cast(str, finding.get("title", ""))
        finding_type = cast(str, finding.get("type", ""))
        group_name = cast(str, get_key_or_fallback(finding, fallback=""))

    org_id = await orgs_domain.get_id_for_group(group_name)
    org_name = await orgs_domain.get_name_by_id(org_id)
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
        - Type: {finding_type}
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


async def send_push_notification(
    user_email: str, title: str, message: str
) -> None:
    user_attrs: dict = await users_domain.get_attributes(
        user_email, ["push_tokens"]
    )
    tokens: List[str] = user_attrs.get("push_tokens", [])

    for token in tokens:
        try:
            notifications_dal.send_push_notification(
                user_email, token, title, message
            )
        except DeviceNotRegisteredError:
            await users_domain.remove_push_token(user_email, token)
