from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async_new,
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
from db_model.findings.enums import (
    FindingStateJustification,
)
from group_access import (
    domain as group_access_domain,
)
from mailer.utils import (
    get_consult_users,
    get_organization_name,
)
from typing import (
    Any,
    List,
)


async def send_mail_comment(
    *,
    context: Any,
    comment_data: CommentType,
    user_mail: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    is_finding_released: bool,
) -> None:
    org_name = await get_organization_name(context, group_name)
    type_: str = comment_data["comment_type"]
    recipients = await get_consult_users(
        group_name=group_name, comment_type=type_
    )
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

    await send_mails_async_new(
        recipients,
        email_context,
        COMMENTS_TAG,
        (
            f"New "
            f'{"observation" if type_ == "observation" else "comment"}'
            f" in finding #{finding_id} for [{group_name}]"
        ),
        "new_comment",
    )


async def send_mail_remove_finding(
    finding_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    justification: FindingStateJustification,
) -> None:
    justification_dict = {
        FindingStateJustification.DUPLICATED: "It is duplicated",
        FindingStateJustification.FALSE_POSITIVE: "It is a false positive",
        FindingStateJustification.NOT_REQUIRED: "Finding not required",
        FindingStateJustification.NO_JUSTIFICATION: "",
    }
    recipients = FI_MAIL_REVIEWERS.split(",")
    mail_context = {
        "analyst_email": discoverer_email,
        "finding_name": finding_name,
        "finding_id": finding_id,
        "justification": justification_dict[justification],
        "group": group_name,
    }
    await send_mails_async_new(
        recipients,
        mail_context,
        GENERAL_TAG,
        f"Finding #{finding_id} in [{group_name}] was removed",
        "delete_finding",
    )


async def send_mail_new_draft(
    context: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    analyst_email: str,
) -> None:
    org_name = await get_organization_name(context, group_name)
    recipients = FI_MAIL_REVIEWERS.split(",")
    email_context: MailContentType = {
        "analyst_email": analyst_email,
        "finding_id": finding_id,
        "finding_name": finding_title,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/drafts/{finding_id}/description"
        ),
        "group": group_name,
        "organization": org_name,
    }
    await send_mails_async_new(
        recipients,
        email_context,
        GENERAL_TAG,
        f"New draft submitted in [{group_name}] - [Finding#{finding_id}]",
        "new_draft",
    )


async def send_mail_new_remediated(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async_new(
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
    await send_mails_async_new(
        recipients,
        email_context,
        GENERAL_TAG,
        f"Draft unsubmitted in [{group_name}] - #{draft_id}",
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
    await send_mails_async_new(
        recipients,
        mail_context,
        VERIFY_TAG,
        f"New remediation in [{group_name}] - [Finding#{finding_id}]",
        "remediate_finding",
    )
