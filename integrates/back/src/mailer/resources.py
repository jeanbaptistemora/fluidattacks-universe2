from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


async def send_mail_handled_file(
    email_to: str,
    group_name: str,
    uploaded: bool,
) -> None:
    if uploaded:
        await send_mails_async_new(
            [email_to],
            group_name,
            GENERAL_TAG,
            f"File uploaded to [{group_name}] in ASM by {email_to}",
            "file_uploaded",
        )
    else:
        await send_mails_async_new(
            [email_to],
            group_name,
            GENERAL_TAG,
            f"File removed from [{group_name}] in ASM",
            "file_uploaded",
        )
