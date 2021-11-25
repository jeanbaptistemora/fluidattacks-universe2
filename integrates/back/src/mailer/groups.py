from .common import (
    COMMENTS_TAG,
    DIGEST_TAG,
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from custom_types import (
    Comment as CommentType,
    MailContent as MailContentType,
)
from mailer.utils import (
    get_organization_name,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    List,
)


async def send_mail_access_granted(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async(
        email_to,
        context,
        GENERAL_TAG,
        f'Access granted to [{context["group"]}] in ASM by Fluid Attacks',
        "access_granted",
    )


async def send_mail_daily_digest(
    email_to: List[str], context: MailContentType
) -> None:
    date = datetime_utils.get_as_str(datetime_utils.get_now(), "%Y/%m/%d")
    # Unique number needed to avoid the email client generating unwanted html
    # code in the template
    context["hash"] = hash((email_to[0], datetime_utils.get_now().timestamp()))
    await send_mails_async(
        email_to,
        context,
        DIGEST_TAG,
        f"Daily Digest ({date})",
        "daily_digest",
    )


async def send_mail_group_report(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async(
        email_to,
        context,
        GENERAL_TAG,
        f'{context["filetype"]} report for [{context["groupname"]}]',
        "group_report",
    )


async def send_mail_comment(
    *,
    loaders: Any,
    comment_data: CommentType,
    user_mail: str,
    recipients: List[str],
    group_name: str = "",
) -> None:
    org_name = await get_organization_name(loaders, group_name)

    email_context: MailContentType = {
        "comment": comment_data["content"].splitlines(),
        "comment_type": "group",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/consulting"
        ),
        "parent": str(comment_data["parent"]),
        "group": group_name,
        "user_email": user_mail,
    }
    await send_mails_async(
        recipients,
        email_context,
        COMMENTS_TAG,
        f"New comment in [{group_name}]",
        "new_comment",
    )


async def send_mail_deactivated_root(
    *,
    email_to: List[str],
    group_name: str,
    root_nickname: str,
    sast_vulns: str,
    dast_vulns: str,
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "group_name": group_name,
            "root_nickname": root_nickname,
            "sast_vulns": sast_vulns,
            "dast_vulns": dast_vulns,
        },
        tags=GENERAL_TAG,
        subject=("Root deactivated"),
        template_name="root_deactivated",
    )
