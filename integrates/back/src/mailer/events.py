from .common import (
    COMMENTS_TAG,
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
from typing import (
    Any,
)


async def send_mail_comment(  # pylint: disable=too-many-locals
    context: Any, comment_data: CommentType, user_mail: str, event_id: str
) -> None:
    event_loader = context.loaders.event
    event = await event_loader.load(event_id)
    group_name = event["project_name"]

    group_loader = context.loaders.group_all
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = context.loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization["name"]

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
        "project": group_name,
        "user_email": user_mail,
    }
    recipients = await get_comment_recipients(group_name, "comment")
    await send_mails_async_new(
        recipients,
        email_context,
        COMMENTS_TAG,
        f"New comment in event #{event_id} for [{group_name}]",
        "new_comment",
    )
