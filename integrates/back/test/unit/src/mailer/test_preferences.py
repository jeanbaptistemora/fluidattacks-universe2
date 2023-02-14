from mailer.preferences import (
    MAIL_PREFERENCES,
)
import pytest
from typing import (
    List,
)


@pytest.mark.parametrize(
    ["notifications", "expected"],
    [
        [
            ["devsecops_agent", "group_alert", "update_group_info"],
            [
                "email_preferences",
                "exclude_trial",
                "only_fluid_staff",
                "roles",
            ],
        ],
    ],
)
def test_mail_preferences(notifications: str, expected: List[str]) -> None:
    for notification in notifications:
        assert list(MAIL_PREFERENCES[notification].keys()) == expected
        assert None not in MAIL_PREFERENCES[notification].values()
