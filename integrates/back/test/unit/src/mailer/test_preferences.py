from mailer.preferences import (
    MAIL_PREFERENCES,
)
from pathlib import (
    Path,
)
import pytest
from typing import (
    List,
)


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
def test_mail_preferences(expected: List[str]) -> None:
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
        assert None not in MAIL_PREFERENCES[notification].values()
