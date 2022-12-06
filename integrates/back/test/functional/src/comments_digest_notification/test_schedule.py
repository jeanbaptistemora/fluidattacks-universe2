# pylint: disable=import-error
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    comments_digest_notification,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("comments_digest_notification")
@freeze_time("2022-11-25T05:00:00.00")
async def test_comments_digest_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(comments_digest_notification, "mail_comments_digest")
    comments_digest_spy = mocker.spy(
        comments_digest_notification, "digest_comments"
    )

    await comments_digest_notification.main()

    assert comments_digest_spy.call_count == 3
    assert mail_spy.call_count == 1
    mail_spy.assert_any_call(
        loaders=mock.ANY,
        context=mock.ANY,
        email_to="johndoe@fluidattacks.com",
        email_cc=[],
    )
