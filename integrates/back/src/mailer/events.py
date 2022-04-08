from .common import (
    COMMENTS_TAG,
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
from db_model.users.get import (
    User,
)
from mailer.utils import (
    get_organization_name,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


async def send_mail_comment(
    *,
    loaders: Any,
    comment_data: CommentType,
    event_id: str,
    recipients: List[str],
    group_name: str,
    user_mail: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)

    email_context: MailContentType = {
        "comment": comment_data["content"].splitlines(),
        "comment_type": "event",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/events/{event_id}/comments"
        ),
        "finding_id": event_id,
        "finding_name": f"Event #{event_id}",
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
        f"New comment in event #{event_id} for [{group_name}]",
        "new_comment",
    )


async def send_mail_event_report(
    *,
    loaders: Any,
    group_name: str = "",
    event_id: str,
    event_type: str,
    description: str,
    is_closed: bool = False,
    report_date: str,
) -> None:
    state: str = "closed" if is_closed else "reported"
    org_name = await get_organization_name(loaders, group_name)
    stakeholders: Tuple[
        Dict[str, Any], ...
    ] = await loaders.group_stakeholders.load(group_name)
    recipients = [stakeholder["email"] for stakeholder in stakeholders]
    users: Tuple[User, ...] = await loaders.user.load_many(recipients)
    users_email = [
        user.email
        for user in users
        if Notification.EVENT_REPORT in user.notifications_preferences.email
    ]
    event_type_format = {
        "AUTHORIZATION_SPECIAL_ATTACK": "Authorization for special attack",
        "CLIENT_APPROVES_CHANGE_TOE": "Client approves ToE change",
        "CLIENT_DETECTS_ATTACK": "Client detects the attack",
        "HIGH_AVAILABILITY_APPROVAL": "High availability approval",
        "INCORRECT_MISSING_SUPPLIES": "Incorrect or missing supplies",
        "OTHER": "Other",
        "TOE_DIFFERS_APPROVED": "ToE different than agreed upon",
    }

    email_context: MailContentType = {
        "group": group_name,
        "event_type": event_type_format[event_type],
        "description": description,
        "event_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/events/"
            f"{event_id}/description"
        ),
        "report_date": report_date,
        "state": state,
    }
    await send_mails_async(
        email_to=users_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(f"Event {state} #[{event_id}] for [{group_name}]"),
        template_name="event_report",
    )
