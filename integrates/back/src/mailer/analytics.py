from .common import (
    GENERAL_TAG,
    get_recipient_first_name,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from dataloaders import (
    Dataloaders,
)
from mailer.types import (
    TrialEngagementInfo,
)
from mailer.utils import (
    get_organization_name,
)


async def send_mail_analytics(
    loaders: Dataloaders, *email_to: str, **context: str
) -> None:
    mail_content = context
    mail_content["live_report_url"] = (
        f'{BASE_URL}/{mail_content["report_entity_percent"]}s/'
        f'{mail_content["report_subject_percent"]}/analytics'
    )
    await send_mails_async(
        loaders,
        list(email_to),
        mail_content,
        GENERAL_TAG,
        (
            f'[ARM] Analytics for [{mail_content["report_subject_title"]}] '
            f'({mail_content["frequency_title"]}: {mail_content["date"]})'
        ),
        "charts_report",
    )


async def send_trial_analytics_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "analytics_link": f"{BASE_URL}/orgs/{org_name}/analytics",
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        tags=[],
        subject=(
            f"[{fname}], check your Continuous Hacking numbers: Analytics."
        ),
        template_name="analytics_notification",
    )
