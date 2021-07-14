from .common import (
    COMMENTS_TAG,
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
    List,
)


async def send_mail_comment(  # pylint: disable=too-many-locals,too-many-statements # noqa: MC0001
    context: Any,
    comment_data: CommentType,
    event_id: str,
    group_name: str,
    recipients: List[str],
    user_mail: str,
) -> None:
    group_loader = context.loaders.group
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
        "group": group_name,
        "user_email": user_mail,
    }
    await send_mails_async_new(
        recipients,
        email_context,
        COMMENTS_TAG,
        f"New comment in event #{event_id} for [{group_name}]",
        "new_comment",
    )
