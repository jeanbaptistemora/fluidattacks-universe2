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
async def test_send_trial_engagement_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_add_stakeholders_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_add_stakeholders_notification",
    )
    mail_send_define_treatments_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_send_define_treatments_notification",
    )
    mail_send_add_repositories_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_send_add_repositories_notification",
    )
    mail_upgrade_squad_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_upgrade_squad_notification",
    )

    await send_trial_engagement_notification.main()

    assert mail_add_stakeholders_notification.await_count == 1
    mail_add_stakeholders_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="janedoe@janedoe.com",
            group_name="testgroup2",
        ),
    )
    assert mail_send_define_treatments_notification.await_count == 1
    mail_send_define_treatments_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="uiguaran@uiguaran.com",
            group_name="testgroup3",
        ),
    )
    assert mail_send_add_repositories_notification.await_count == 1
    mail_send_add_repositories_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="abuendia@abuendia.com",
            group_name="testgroup4",
        ),
    )
    assert mail_upgrade_squad_notification.await_count == 1
    mail_upgrade_squad_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="johndoe@johndoe.com",
            group_name="testgroup",
        ),
    )
