from .common import (
    COMMENTS_TAG,
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
