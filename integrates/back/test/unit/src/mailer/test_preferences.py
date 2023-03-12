from db_model.enums import (
    Notification,
)
from mailer.preferences import (
    MAIL_PREFERENCES,
)
from pathlib import (
    Path,
)
import pytest


@pytest.mark.parametrize(
    ["expected"],
    [
        [
            [
                "email_preferences",
                "exclude_trial",
                "only_fluid_staff",
                "roles",
            ],
        ],
    ],
)
def test_mail_preferences(expected: list[str]) -> None:
    entries = Path("back/src/mailer/email_templates")
    notifications = {
        entry.name.removesuffix(".html")
        for entry in entries.iterdir()
        if entry.name.endswith(".html")
    }
    assert len(notifications) == len(MAIL_PREFERENCES)
    assert sorted(MAIL_PREFERENCES.keys()) == list(MAIL_PREFERENCES.keys())
    for notification in notifications:
        assert list(MAIL_PREFERENCES[notification].keys()) == expected
    assert all(
        (
            item["email_preferences"] in list(Notification.__members__)
            or item["email_preferences"] is None
        )
        for item in MAIL_PREFERENCES.values()
    )
