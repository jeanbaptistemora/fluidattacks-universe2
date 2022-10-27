# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    abandoned_trial_notification,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("abandoned_trial_notification")
@freeze_time("2022-11-11T15:58:31.280182")
async def test_abandoned_trial_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(
        abandoned_trial_notification, "mail_abandoned_trial_notification"
    )

    await abandoned_trial_notification.main()

    assert mail_spy.await_count == 2
    mail_spy.assert_any_call(mock.ANY, "janedoe@fluidattacks.com", True)
    mail_spy.assert_any_call(mock.ANY, "uiguaran@fluidattacks.com", False)
