from freezegun import (
    freeze_time,
)
import pytest
from schedulers.treatment_alert_notification import (
    days_to_end,
    ExpiringDataType,
    unique_emails,
)

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2022-12-07T00:00:00.0")
def test_days_to_end() -> None:
    assert days_to_end("2022-12-12") == 5


@pytest.mark.parametrize(
    ["groups_data"],
    [
        [
            {
                "oneshottest": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "customer_manager@fluidattacks.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "integratesuser@gmail.com",
                    ),
                    "group_expiring_findings": {},
                },
                "unittesting": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "continuoushacking@gmail.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "unittest2@fluidattacks.com",
                    ),
                    "group_expiring_findings": {},
                },
            }
        ],
    ],
)
def test_unique_emails(
    groups_data: dict[str, ExpiringDataType],
) -> None:
    emails = unique_emails(dict(groups_data), ())
    assert len(emails) == 9
