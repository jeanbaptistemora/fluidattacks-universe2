# pylint: disable=import-error
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    upgrade_squad_notification,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upgrade_squad_notification")
@freeze_time("2022-11-11T15:58:31.280182")
async def test_abandoned_trial_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(
        upgrade_squad_notification, "mail_upgrade_squad_notification"
    )

    await upgrade_squad_notification.main()

    assert mail_spy.await_count == 1
    mail_spy.assert_any_call(mock.ANY, "johndoe@johndoe.com")
