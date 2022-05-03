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
    MailContent as MailContentType,
)
from datetime import (
    date,
)
from db_model.enums import (
    Notification,
)
from db_model.groups.types import (
    Group,
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
    Optional,
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
    report_date = datetime_utils.get_as_str(
        datetime_utils.get_now(), "%Y/%m/%d"
    )
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
        f"Daily Digest ({report_date})",
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
    comment_data: Dict[str, Any],
    user_mail: str,
    recipients: List[str],
    group_name: str = "",
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    group: Group = await loaders.group_typed.load(group_name)
    has_machine: bool = group.state.has_machine
    has_squad: bool = group.state.has_squad

    email_context: MailContentType = {
        "comment": str(comment_data["content"]).splitlines(),
        "comment_type": "group",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/consulting"
        ),
        "parent": str(comment_data["parent"]),
        "group": group_name,
        "has_machine": has_machine,
        "has_squad": has_squad,
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


async def send_mail_added_root(
    *,
    branch: str,
    email_to: List[str],
    environment: str,
    group_name: str,
    root_nickname: str,
    responsible: str,
    modified_date: str,
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "branch": branch.capitalize(),
            "environment": environment.capitalize(),
            "group": group_name,
            "root_nickname": root_nickname,
            "responsible": responsible,
            "date": str(datetime_utils.get_date_from_iso_str(modified_date)),
        },
        tags=GENERAL_TAG,
        subject=f"Root added in [{group_name}]",
        template_name="root_added",
    )


async def send_mail_updated_root(
    *,
    email_to: List[str],
    group_name: str,
    responsible: str,
    root_nickname: str,
    new_root_content: Dict[str, Any],
    old_state: Dict[str, Any],
    modified_date: str,
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "new_root_content": new_root_content,
            "old_state": old_state,
            "root_nickname": root_nickname,
            "date": str(datetime_utils.get_date_from_iso_str(modified_date)),
        },
        tags=GENERAL_TAG,
        subject=f"Root have been changed in [{group_name}]",
        template_name="updated_root",
    )


async def send_mail_deactivated_root(
    *,
    activated_by: str,
    email_to: List[str],
    group_name: str,
    last_clone_date: str,
    last_root_state: str,
    other: Optional[str],
    reason: str,
    root_age: int,
    root_nickname: str,
    **kwargs: str,
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "group": group_name,
            "reason": other
            if other
            else reason.replace("_", " ").capitalize(),
            "root_age": root_age,
            "activated_by": activated_by,
            "root_nickname": root_nickname,
            "last_root_state": last_root_state.capitalize(),
            "last_clone_date": last_clone_date,
            "sast_vulns": kwargs["sast_vulns"],
            "dast_vulns": kwargs["dast_vulns"],
            "responsible": kwargs["responsible"],
        },
        tags=GENERAL_TAG,
        subject=("Root deactivated"),
        template_name="root_deactivated",
    )


async def send_mail_root_file_report(
    *,
    group_name: str,
    responsible: str,
    is_added: bool = False,
    file_name: str,
    file_description: str,
    report_date: date,
    email_to: List[str],
) -> None:
    state_format: str = "added" if is_added else "deleted"
    await send_mails_async(
        email_to=email_to,
        context={
            "state": state_format,
            "group_name": group_name,
            "responsible": responsible,
            "file_name": file_name,
            "file_description": file_description,
            "report_date": report_date,
        },
        tags=GENERAL_TAG,
        subject=(f"Root file {state_format}"),
        template_name="root_file_report",
    )


async def send_mail_environment_report(
    *,
    email_to: List[str],
    group_name: str,
    responsible: str,
    git_root: str,
    urls_added: List[str],
    urls_deleted: List[str],
    modified_date: str,
) -> None:
    await send_mails_async(
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "git_root": git_root,
            "urls_added": urls_added,
            "urls_deleted": urls_deleted,
            "report_date": str(
                datetime_utils.get_date_from_iso_str(modified_date)
            ),
        },
        tags=GENERAL_TAG,
        subject=f"Environment have been modified in [{group_name}]",
        template_name="environment_report",
    )


async def send_mail_updated_policies(
    *, email_to: List[str], context: Dict[str, Any]
) -> None:
    await send_mails_async(
        email_to,
        context,
        GENERAL_TAG,
        f'Policies has been changed in [{context["org_name"]}]',
        "updated_policies",
    )


async def send_mail_reminder(
    *,
    context: MailContentType,
    email_to: List[str],
) -> None:
    await send_mails_async(
        email_to=email_to,
        tags=GENERAL_TAG,
        subject="Reminder",
        context=context,
        template_name="reminder_notification",
    )
