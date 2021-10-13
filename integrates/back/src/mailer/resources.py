from .common import (
    GENERAL_TAG,
    send_mails_async,
)


async def send_mail_handled_file(
    email_to: str,
    group_name: str,
    file_name: str,
    uploaded: bool,
) -> None:
    mail_context = {
        "file_name": file_name,
        "group": group_name,
    }

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
