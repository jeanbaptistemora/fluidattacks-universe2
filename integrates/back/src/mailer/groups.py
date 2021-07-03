from .common import (
    COMMENTS_TAG,
    DIGEST_TAG,
    GENERAL_TAG,
    get_comment_recipients,
    send_mails_async_new,
)
from context import (
    BASE_URL,
)
from custom_types import (
    Comment as CommentType,
    MailContent as MailContentType,
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
    await send_mails_async_new(
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
    await send_mails_async_new(
        email_to,
        context,
        DIGEST_TAG,
        f"Daily Digest ({date})",
        "daily_digest",
    )


async def send_mail_group_report(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'{context["filetype"]} report for [{context["groupname"]}]',
        "group_report",
    )


async def send_mail_comment(  # pylint: disable=too-many-locals
    context: Any,
    comment_data: CommentType,
    user_mail: str,
    group_name: str = "",
) -> None:
    group_loader = context.loaders.group
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = context.loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization["name"]

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
    recipients = await get_comment_recipients(group_name, "comment")
    await send_mails_async_new(
        recipients,
        email_context,
        COMMENTS_TAG,
        f"New comment in [{group_name}]",
        "new_comment",
    )
