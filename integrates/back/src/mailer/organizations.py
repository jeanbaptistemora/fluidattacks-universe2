from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from dataloaders import (
    Dataloaders,
)
from typing import (
    Any,
)


async def send_mail_updated_policies(
    *, loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
) -> None:
    context["user_role"] = str(context["user_role"]).replace("_", " ")
    await send_mails_async(
        loaders,
        email_to,
        context=context,
        tags=GENERAL_TAG,
        subject="[ARM] Policies have been changed in "
        + f'[{context["entity_name"]}]',
        template_name="updated_policies",
    )
