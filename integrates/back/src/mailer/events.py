from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_REVIEWERS,
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
from db_model.roots.types import (
    GitRoot,
)
from db_model.stakeholders.types import (
    Stakeholder,
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


async def send_mail_comment(
    *,
    loaders: Any,
    comment_data: Dict[str, Any],
    event_id: str,
    recipients: List[str],
    group_name: str,
    user_mail: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    group: Group = await loaders.group.load(group_name)
    has_machine: bool = group.state.has_machine
    has_squad: bool = group.state.has_squad

    email_context: dict[str, Any] = {
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
        "has_squad": has_squad,
        "user_email": user_mail,
    }
    stakeholders: Tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.NEW_COMMENT
        in stakeholder.notifications_preferences.email
    ]
    reviewers = FI_MAIL_REVIEWERS.split(",")
    customer_success_recipients = FI_MAIL_CUSTOMER_SUCCESS.split(",")
    await send_mails_async(
        loaders,
        [*stakeholders_email, *customer_success_recipients, *reviewers],
        email_context,
        COMMENTS_TAG,
        f"[ASM] New comment in event #{event_id} for [{group_name}]",
        "new_comment",
    )


async def send_mail_event_report(  # pylint: disable=too-many-locals
    *,
    loaders: Any,
    group_name: str = "",
    event_id: str,
    event_type: str,
    description: str,
    root_id: Optional[str],
    reason: Optional[str] = None,
    other: Optional[str] = None,
    is_closed: bool = False,
    reminder_notification: bool = False,
    report_date: date,
) -> None:
    state: str = "closed" if is_closed else "reported"
    reason_format = (
        other
        if other
        else str(reason).replace("_", " ").capitalize()
        if reason
        else ""
    )
    event_age: int = (datetime_utils.get_now().date() - report_date).days
    org_name = await get_organization_name(loaders, group_name)

    group_stakeholders: Tuple[
        Stakeholder, ...
    ] = await loaders.group_stakeholders.load(group_name)
    recipients = [stakeholder.email for stakeholder in group_stakeholders]
    stakeholders: Tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.EVENT_REPORT
        in stakeholder.notifications_preferences.email
    ]

    event_type_format = {
        "AUTHORIZATION_SPECIAL_ATTACK": "Authorization for special attack",
        "INCORRECT_MISSING_SUPPLIES": "Incorrect or missing supplies",
        "OTHER": "Other",
        "TOE_DIFFERS_APPROVED": "ToE different than agreed upon",
        "DATA_UPDATE_REQUIRED": "Request user modification/workflow update",
    }

    root = await loaders.root.load((group_name, root_id)) if root_id else None
    root_url: Optional[str] = (
        root.state.url if root and isinstance(root, GitRoot) else None
    )

    email_context: dict[str, Any] = {
        "group": group_name.lower(),
        "event_type": event_type_format[event_type],
        "description": description.strip("."),
        "event_age": event_age,
        "event_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/events/"
            f"{event_id}/description"
        ),
        "reason": reason_format,
        "reminder_notification": reminder_notification,
        "report_date": str(report_date),
        "root_url": root_url,
        "state": state,
    }

    subject: str = (
        f"[ASM] Event solved #[{event_id}] for [{group_name}]"
        if is_closed
        else f"[ASM] ACTION NEEDED: Your group [{group_name}] is at risk"
    )

    await send_mails_async(
        loaders=loaders,
        email_to=stakeholders_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=subject,
        template_name="event_report",
    )
