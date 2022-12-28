from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    FI_MAIL_TELEMARKETING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
from typing import (
    Any,
)


async def send_mail_to_get_squad_plan(
    loaders: Dataloaders,
    name: str,
    email: str,
    phone: StakeholderPhone,
) -> None:
    email_context: dict[str, Any] = {
        "empty_notification_notice": True,
        "national_number": (
            f"+{phone.calling_country_code} {phone.national_number}"
        ),
        "lead_name": name,
        "lead_email": email,
    }
    await send_mails_async(
        loaders,
        email_to=[FI_MAIL_TELEMARKETING],
        context=email_context,
        tags=GENERAL_TAG,
        subject="[ARM] New lead assigned",
        template_name="contact_sales_onboarding",
    )
