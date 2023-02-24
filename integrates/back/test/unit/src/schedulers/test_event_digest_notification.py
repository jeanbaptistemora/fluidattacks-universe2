from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from freezegun import (
    freeze_time,
)
import pytest
from pytz import (
    UTC,
)
from schedulers.event_digest_notification import (
    EventsDataType,
    filter_last_event_comments,
    get_days_since_comment,
    unique_emails,
)

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2022-12-07T00:00:00.0")
def test_get_days_since_comment() -> None:
    assert (
        get_days_since_comment(datetime(2022, 12, 1).replace(tzinfo=UTC)) == 6
    )


@pytest.mark.parametrize(
    ["comments"],
    [
        [
            [
                EventComment(
                    event_id="418900971",
                    id="1545946228675",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 1, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
                EventComment(
                    event_id="540462628",
                    id="1545946228676",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 2, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
                EventComment(
                    event_id="418900979",
                    id="1545946228677",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 4, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
            ]
        ],
    ],
)
@freeze_time("2022-12-05T06:00:00.0")
def test_filter_last_event_comments(
    *,
    comments: list[EventComment],
) -> None:
    assert len(filter_last_event_comments(comments)) == 2


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
                    "events": (),
                    "events_comments": {},
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
                    "events": (),
                    "events_comments": {},
                },
            }
        ],
    ],
)
def test_unique_emails(
    groups_data: dict[str, EventsDataType],
) -> None:
    emails = unique_emails(dict(groups_data), ())
    assert len(emails) == 9
