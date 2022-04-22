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
    group: Group = await loaders.group_typed.load(group_name)
    has_machine: bool = group.state.has_machine

    email_context: MailContentType = {
        "comment": str(comment_data["content"]).splitlines(),
        "comment_type": "event",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/events/{event_id}/comments"
        ),
        "finding_id": event_id,
        "finding_name": f"Event #{event_id}",
        "parent": str(comment_data["parent"]),
        "group": group_name,
        "has_machine": has_machine,
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


async def send_mail_event_report(  # pylint: disable=too-many-locals
    *,
    loaders: Any,
    group_name: str = "",
    event_id: str,
    event_type: str,
    description: str,
    is_closed: bool = False,
    report_date: date,
) -> None:
    state: str = "closed" if is_closed else "reported"
    event_age: int = (datetime_utils.get_now().date() - report_date).days
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
        "INCORRECT_MISSING_SUPPLIES": "Incorrect or missing supplies",
        "OTHER": "Other",
        "TOE_DIFFERS_APPROVED": "ToE different than agreed upon",
    }

    email_context: MailContentType = {
        "group": group_name.capitalize(),
        "event_type": event_type_format[event_type],
        "description": description,
        "event_age": event_age,
        "event_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/events/"
            f"{event_id}/description"
        ),
        "report_date": str(report_date),
        "state": state,
    }
    await send_mails_async(
        email_to=users_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(f"Event {state} #[{event_id}] for [{group_name}]"),
        template_name="event_report",
    )
