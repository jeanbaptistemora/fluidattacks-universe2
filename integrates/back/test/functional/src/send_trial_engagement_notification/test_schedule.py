# pylint: disable=import-error
from datetime import (
    datetime,
)
from freezegun import (
    freeze_time,
)
from mailer.types import (
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
    mail_support_channels_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_support_channels_notification",
    )
    mail_devsecops_agent_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_devsecops_agent_notification",
    )
    mail_trial_reports_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_trial_reports_notification",
    )
    mail_upgrade_squad_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_upgrade_squad_notification",
    )
    mail_trial_ending_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_trial_ending_notification",
    )
    mail_how_improve_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_how_improve_notification",
    )
    mail_trial_ended_notification = mocker.spy(
        send_trial_engagement_notification,
        "mail_trial_ended_notification",
    )

    await send_trial_engagement_notification.main()

    assert mail_add_stakeholders_notification.await_count == 1
    mail_add_stakeholders_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="janedoe@janedoe.com",
            group_name="testgroup2",
            start_date=datetime.fromisoformat(
                "2022-11-08T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_send_define_treatments_notification.await_count == 1
    mail_send_define_treatments_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="uiguaran@uiguaran.com",
            group_name="testgroup3",
            start_date=datetime.fromisoformat(
                "2022-11-06T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_send_add_repositories_notification.await_count == 1
    mail_send_add_repositories_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="abuendia@abuendia.com",
            group_name="testgroup4",
            start_date=datetime.fromisoformat(
                "2022-11-04T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_support_channels_notification.await_count == 1
    mail_support_channels_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="avicario@avicario.com",
            group_name="testgroup5",
            start_date=datetime.fromisoformat(
                "2022-11-02T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_devsecops_agent_notification.await_count == 1
    mail_devsecops_agent_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="snassar@snassar.com",
            group_name="testgroup7",
            start_date=datetime.fromisoformat(
                "2022-10-29T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_trial_reports_notification.await_count == 1
    mail_trial_reports_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="jbuendia@jbuendia.com",
            group_name="testgroup8",
            start_date=datetime.fromisoformat(
                "2022-10-27T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_upgrade_squad_notification.await_count == 1
    mail_upgrade_squad_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="johndoe@johndoe.com",
            group_name="testgroup",
            start_date=datetime.fromisoformat(
                "2022-10-25T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_trial_ending_notification.await_count == 1
    mail_trial_ending_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="rremedios@rremedios.com",
            group_name="testgroup9",
            start_date=datetime.fromisoformat(
                "2022-10-23T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_how_improve_notification.await_count == 1
    mail_how_improve_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="rmontiel@rmontiel.com",
            group_name="testgroup10",
            start_date=datetime.fromisoformat(
                "2022-10-22T15:58:31.280182+00:00"
            ),
        ),
    )
    assert mail_trial_ended_notification.await_count == 1
    mail_trial_ended_notification.assert_any_call(
        mock.ANY,
        TrialEngagementInfo(
            email_to="rmoscote@rmoscote.com",
            group_name="testgroup11",
            start_date=datetime.fromisoformat(
                "2022-10-20T15:58:31.280182+00:00"
            ),
        ),
    )
