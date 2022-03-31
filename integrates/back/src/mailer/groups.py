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
from db_model.enums import (
    Notification,
)
from db_model.users.types import (
    User,
)
from mailer.utils import (
    get_organization_name,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
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
        is_access_granted=True,
    )


async def send_mail_daily_digest(
    loaders: Any, email_to: List[str], context: MailContentType
) -> None:
    date = datetime_utils.get_as_str(datetime_utils.get_now(), "%Y/%m/%d")
    # Unique number needed to avoid the email client generating unwanted html
    # code in the template
    context["hash"] = hash((email_to[0], datetime_utils.get_now().timestamp()))
    users: Tuple[User, ...] = await loaders.user.load_many(email_to)
    users_email = [
        user.email
        for user in users
        if Notification.DAILY_DIGEST in user.notifications_preferences.email
    ]
    await send_mails_async(
        users_email,
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
    users: Tuple[User, ...] = await loaders.user.load_many(recipients)
    users_email = [
        user.email
        for user in users
        if Notification.NEW_COMMENT in user.notifications_preferences.email
    ]
    await send_mails_async(
        users_email,
        email_context,
        COMMENTS_TAG,
        f"New comment in [{group_name}]",
        "new_comment",
    )


async def send_mail_deactivated_root(
    *,
    email_to: List[str],
    group_name: str,
    other: str,
    reason: str,
    root_age: int,
    root_nickname: str,
    **kwargs: Dict[str, str],
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "group": group_name,
            "reason": other
            if other
            else reason.replace("_", " ").capitalize(),
            "root_age": root_age,
            "root_nickname": root_nickname,
            "sast_vulns": kwargs["sast_vulns"],
            "dast_vulns": kwargs["dast_vulns"],
            "responsible": kwargs["responsible"],
        },
        tags=GENERAL_TAG,
        subject=("Root deactivated"),
        template_name="root_deactivated",
    )


async def send_mail_updated_policies(
    email_to: List[str], context: MailContentType
) -> None:
    await send_mails_async(
        email_to,
        context,
        GENERAL_TAG,
        f'A policies has been changed in [{context["org_name"]}]',
        "updated_policies",
    )
