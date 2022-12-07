# pylint: disable=import-error
from freezegun import (
    freeze_time,
)
from mailer.groups import (
    TrialEngagementInfo,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    send_trial_engagement_notification,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("send_trial_engagement_notification")
@freeze_time("2022-11-11T15:58:31.280182")
async def test_abandoned_trial_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_upgrade_squad_notification = mocker.spy(
        send_trial_engagement_notification, "mail_upgrade_squad_notification"
    )

    await send_trial_engagement_notification.main()

    assert mail_upgrade_squad_notification.await_count == 1
    mail_upgrade_squad_notification.assert_any_call(
        mock.ANY, TrialEngagementInfo(email_to="johndoe@johndoe.com")
    )
