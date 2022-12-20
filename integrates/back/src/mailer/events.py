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
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date,
)
from db_model.enums import (
    Notification,
)
from db_model.event_comments.types import (
    EventComment,
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
from group_access.domain import (
    get_group_stakeholders_emails,
)
from mailer.utils import (
    get_organization_name,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Optional,
)


async def send_mail_comment(
    *,
    loaders: Dataloaders,
    comment_data: EventComment,
    event_id: str,
    recipients: list[str],
    group_name: str,
    user_mail: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    group: Group = await loaders.group.load(group_name)
    has_machine: bool = group.state.has_machine
    has_squad: bool = group.state.has_squad

    email_context: dict[str, Any] = {
        "comment": comment_data.content.splitlines(),
        "comment_type": "event",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/events/{event_id}/comments"
        ),
        "finding_id": event_id,
        "finding_name": f"Event #{event_id}",
        "parent": comment_data.parent_id,
        "group": group_name,
        "has_machine": has_machine,
        "has_squad": has_squad,
        "user_email": user_mail,
    }
    stakeholders: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.NEW_COMMENT
        in stakeholder.state.notifications_preferences.email
    ]
    reviewers = FI_MAIL_REVIEWERS.split(",")
    customer_success_recipients = FI_MAIL_CUSTOMER_SUCCESS.split(",")
    await send_mails_async(
        loaders,
        [*stakeholders_email, *customer_success_recipients, *reviewers],
        email_context,
        COMMENTS_TAG,
        f"[ARM] New comment in event #{event_id} for [{group_name}]",
        "new_comment",
    )


async def send_mail_event_report(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
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
    state: str = "solved" if is_closed else "reported"
    reason_format = (
        other
        if other
        else str(reason).replace("_", " ").capitalize()
        if reason
        else ""
    )
    event_age: int = (datetime_utils.get_now().date() - report_date).days
    org_name = await get_organization_name(loaders, group_name)

    recipients: list[str] = await get_group_stakeholders_emails(
        loaders, group_name
    )
    stakeholders: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.EVENT_REPORT
        in stakeholder.state.notifications_preferences.email
    ]

    event_type_format = {
        "AUTHORIZATION_SPECIAL_ATTACK": "Authorization for a special attack",
        "CLIENT_CANCELS_PROJECT_MILESTONE": (
            "The client cancels a project milestone"
        ),
        "CLIENT_EXPLICITLY_SUSPENDS_PROJECT": (
            "The client suspends the project"
        ),
        "CLONING_ISSUES": "Cloning issues",
        "CREDENTIAL_ISSUES": "Credentials issues",
        "DATA_UPDATE_REQUIRED": "Request user modification/workflow update",
        "ENVIRONMENT_ISSUES": "Environment issues",
        "INSTALLER_ISSUES": "Installer issues",
        "MISSING_SUPPLIES": "Missing supplies",
        "NETWORK_ACCESS_ISSUES": "Network access issues",
        "OTHER": "Other",
        "REMOTE_ACCESS_ISSUES": "Remote access issues",
        "TOE_DIFFERS_APPROVED": "ToE different than agreed upon",
        "VPN_ISSUES": "VPN issues",
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
        f"[ARM] Event #[{event_id}] was solved in [{group_name}]"
        if is_closed
        else f"[ARM] ACTION NEEDED: Your group [{group_name}] is at risk"
    )

    await send_mails_async(
        loaders=loaders,
        email_to=stakeholders_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=subject,
        template_name="event_report",
    )
