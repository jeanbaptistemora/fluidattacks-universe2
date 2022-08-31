from dataloaders import (
    get_new_context,
)
from schedulers.missing_environment_alert import (
    _send_mail_report as send_mail_missing_environment,
)


async def test_send_mail_missing_environment() -> None:
    await send_mail_missing_environment(
        loaders=get_new_context(),
        group="unittesting",
        group_date_delta=3,
    )
