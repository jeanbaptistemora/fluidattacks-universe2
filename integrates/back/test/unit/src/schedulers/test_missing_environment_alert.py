from dataloaders import (
    get_new_context,
)
import pytest
from schedulers.missing_environment_alert import (
    _send_mail_report as send_mail_missing_environment,
    has_environment,
)


@pytest.mark.asyncio
async def test_send_mail_missing_environment() -> None:
    await send_mail_missing_environment(
        loaders=get_new_context(),
        group="unittesting",
        group_date_delta=3,
    )


@pytest.mark.asyncio
async def test_has_environment() -> None:
    loaders = get_new_context()
    group = "unittesting"
    test = await has_environment(loaders, group)
    assert test is True
