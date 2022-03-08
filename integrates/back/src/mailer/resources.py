from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from db_model.enums import (
    Notification,
)
from db_model.users.get import (
    User,
)
from typing import (
    Any,
)


async def send_mail_handled_file(
    loaders: Any,
    email_to: str,
    group_name: str,
    file_name: str,
    uploaded: bool,
) -> None:
    mail_context = {
        "file_name": file_name,
        "group": group_name,
    }

    user: User = await loaders.user.load(email_to)
    if Notification.FILE_UPLOADED in user.notifications_preferences.email:
        if uploaded:
            await send_mails_async(
                [email_to],
                mail_context,
                GENERAL_TAG,
                f"File uploaded to [{group_name}] in ASM by {email_to}",
                "file_uploaded",
            )
        else:
            await send_mails_async(
                [email_to],
                mail_context,
                GENERAL_TAG,
                f"File removed from [{group_name}] in ASM",
                "file_removed",
            )
