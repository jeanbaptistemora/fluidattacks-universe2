from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async,
    VERIFY_TAG,
)
from context import (
    BASE_URL,
    FI_MAIL_REVIEWERS,
)
from custom_types import (
    Comment as CommentType,
    MailContent as MailContentType,
)
from db_model.enums import (
    StateRemovalJustification,
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
)


async def send_mail_comment(
    *,
    loaders: Any,
    comment_data: CommentType,
    user_mail: str,
    finding_id: str,
    finding_title: str,
    recipients: List[str],
    group_name: str,
    is_finding_released: bool,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    type_: str = comment_data["comment_type"]
    email_context: MailContentType = {
        "comment": comment_data["content"].splitlines(),
        "comment_type": type_,
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/"
            f'{"vulns" if is_finding_released else "drafts"}/{finding_id}/'
            f'{"consulting" if type_ == "comment" else "observations"}'
        ),
        "finding_id": finding_id,
        "finding_name": finding_title,
        "parent": str(comment_data["parent"]),
        "group": group_name,
        "user_email": user_mail,
    }

    await send_mails_async(
        recipients,
        email_context,
        COMMENTS_TAG,
        (
            f'New {"observation" if type_ == "observation" else "comment"}'
            f" in [{finding_title}] for [{group_name}]"
        ),
        "new_comment",
    )


async def send_mail_remove_finding(
    finding_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    justification: StateRemovalJustification,
) -> None:
    justification_dict = {
        StateRemovalJustification.DUPLICATED: "It is duplicated",
        StateRemovalJustification.FALSE_POSITIVE: "It is a false positive",
        StateRemovalJustification.NO_JUSTIFICATION: "",
        StateRemovalJustification.NOT_REQUIRED: "Finding not required",
        StateRemovalJustification.REPORTING_ERROR: "It is a reporting error",
    }
    recipients = FI_MAIL_REVIEWERS.split(",")
    mail_context = {
        "hacker_email": discoverer_email,
        "finding_name": finding_name,
        "finding_id": finding_id,
        "justification": justification_dict[justification],
        "group": group_name,
    }
    await send_mails_async(
        recipients,
        mail_context,
        GENERAL_TAG,
        f"Finding removed [{finding_name}] in [{group_name}]",
        "delete_finding",
    )


async def send_mail_new_draft(
    context: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    hacker_email: str,
) -> None:
    org_name = await get_organization_name(context, group_name)
    recipients = FI_MAIL_REVIEWERS.split(",")
    email_context: MailContentType = {
        "hacker_email": hacker_email,
        "finding_id": finding_id,
        "finding_name": finding_title,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/drafts/{finding_id}/description"
        ),
        "group": group_name,
        "organization": org_name,
    }
    await send_mails_async(
        recipients,
        email_context,
        GENERAL_TAG,
        f"Draft submitted [{finding_title}] in [{group_name}]",
        "new_draft",
    )


async def send_mail_new_remediated(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async(
        email_to,
        context,
        GENERAL_TAG,
        f'Findings to verify ({context["total"]})',
        "new_remediated",
    )


async def send_mail_reject_draft(  # pylint: disable=too-many-arguments
    context: Any,
    draft_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    reviewer_email: str,
) -> None:
    org_name = await get_organization_name(context, group_name)
    recipients = FI_MAIL_REVIEWERS.split(",")
    recipients.append(discoverer_email)
    email_context: MailContentType = {
        "admin_mail": reviewer_email,
        "analyst_mail": discoverer_email,
        "draft_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/drafts/{draft_id}/description"
        ),
        "finding_id": draft_id,
        "finding_name": finding_name,
        "group": group_name,
        "organization": org_name,
    }
    await send_mails_async(
        recipients,
        email_context,
        GENERAL_TAG,
        f"Draft unsubmitted [{finding_name}] in [{group_name}]",
        "unsubmitted_draft",
    )


async def send_mail_remediate_finding(  # pylint: disable=too-many-arguments
    context: Any,
    user_email: str,
    finding_id: str,
    finding_name: str,
    group_name: str,
    justification: str,
) -> None:
    org_name = await get_organization_name(context, group_name)
    recipients = await group_access_domain.get_reattackers(group_name)
    mail_context = {
        "group": group_name.lower(),
        "organization": org_name,
        "finding_name": finding_name,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}/locations"
        ),
        "finding_id": finding_id,
        "user_email": user_email,
        "solution_description": justification.splitlines(),
    }
    await send_mails_async(
        recipients,
        mail_context,
        VERIFY_TAG,
        f"New remediation for [{finding_name}] in [{group_name}]",
        "remediate_finding",
    )
