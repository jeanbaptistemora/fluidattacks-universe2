from datetime import (
    datetime,
    timezone,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidences,
    EventState,
    EventUnreliableIndicators,
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
    get_open_events,
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
    ["events"],
    [
        [
            [
                Event(
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime(
                        2018, 6, 27, 19, 40, 5, tzinfo=timezone.utc
                    ),
                    description="Integrates unit test",
                    event_date=datetime(
                        2018, 6, 27, 12, 0, tzinfo=timezone.utc
                    ),
                    evidences=EventEvidences(
                        file_1=None,
                        image_1=None,
                        image_2=None,
                        image_3=None,
                        image_4=None,
                        image_5=None,
                        image_6=None,
                    ),
                    group_name="unittesting",
                    hacker="unittest@fluidattacks.com",
                    id="418900971",
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime(
                            2018,
                            6,
                            27,
                            19,
                            40,
                            5,
                            tzinfo=timezone.utc,
                        ),
                        status=EventStateStatus.CREATED,
                        comment_id=None,
                        other=None,
                        reason=None,
                    ),
                    type=EventType.OTHER,
                    root_id=None,
                    unreliable_indicators=EventUnreliableIndicators(
                        unreliable_solving_date=None
                    ),
                ),
                Event(
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime(
                        2018, 12, 17, 21, 21, 3, tzinfo=timezone.utc
                    ),
                    description="Unit testing event",
                    event_date=datetime(
                        2018, 12, 17, 21, 20, tzinfo=timezone.utc
                    ),
                    evidences=EventEvidences(
                        file_1=None,
                        image_1=None,
                        image_2=None,
                        image_3=None,
                        image_4=None,
                        image_5=None,
                        image_6=None,
                    ),
                    group_name="unittesting",
                    hacker="unittest@fluidattacks.com",
                    id="463578352",
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime(
                            2018, 12, 26, 18, 37, tzinfo=timezone.utc
                        ),
                        status=EventStateStatus.SOLVED,
                        comment_id=None,
                        other=None,
                        reason=None,
                    ),
                    type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
                    root_id=None,
                    unreliable_indicators=EventUnreliableIndicators(
                        unreliable_solving_date=datetime(
                            2018, 12, 26, 18, 37, tzinfo=timezone.utc
                        )
                    ),
                ),
                Event(
                    client="Fluid Attacks",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime(
                        2019, 3, 11, 15, 57, 45, tzinfo=timezone.utc
                    ),
                    description="This is an eventuality",
                    event_date=datetime(
                        2020, 3, 11, 14, 0, tzinfo=timezone.utc
                    ),
                    evidences=EventEvidences(
                        file_1=None,
                        image_1=None,
                        image_2=None,
                        image_3=None,
                        image_4=None,
                        image_5=None,
                        image_6=None,
                    ),
                    group_name="unittesting",
                    hacker="unittest@fluidattacks.com",
                    id="484763304",
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime(
                            2020, 4, 11, 18, 37, tzinfo=timezone.utc
                        ),
                        status=EventStateStatus.SOLVED,
                        comment_id=None,
                        other=None,
                        reason=None,
                    ),
                    type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
                    root_id=None,
                    unreliable_indicators=EventUnreliableIndicators(
                        unreliable_solving_date=datetime(
                            2020, 4, 11, 18, 37, tzinfo=timezone.utc
                        )
                    ),
                ),
                Event(
                    client="test",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime(
                        2019, 9, 19, 15, 43, 43, tzinfo=timezone.utc
                    ),
                    description="Testing Event",
                    event_date=datetime(
                        2019, 9, 19, 13, 9, tzinfo=timezone.utc
                    ),
                    evidences=EventEvidences(
                        file_1=None,
                        image_1=None,
                        image_2=None,
                        image_3=None,
                        image_4=None,
                        image_5=None,
                        image_6=None,
                    ),
                    group_name="unittesting",
                    hacker="unittest@fluidattacks.com",
                    id="538745942",
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime(
                            2019,
                            9,
                            19,
                            15,
                            43,
                            43,
                            tzinfo=timezone.utc,
                        ),
                        status=EventStateStatus.CREATED,
                        comment_id=None,
                        other=None,
                        reason=None,
                    ),
                    type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
                    root_id=None,
                    unreliable_indicators=EventUnreliableIndicators(
                        unreliable_solving_date=None
                    ),
                ),
                Event(
                    client="Fluid Attacks",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime(
                        2019, 9, 25, 14, 36, 27, tzinfo=timezone.utc
                    ),
                    description="Testing",
                    event_date=datetime(2019, 4, 2, 8, 2, tzinfo=timezone.utc),
                    evidences=EventEvidences(
                        file_1=None,
                        image_1=None,
                        image_2=None,
                        image_3=None,
                        image_4=None,
                        image_5=None,
                        image_6=None,
                    ),
                    group_name="unittesting",
                    hacker="unittest@fluidattacks.com",
                    id="540462628",
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime(
                            2019,
                            9,
                            25,
                            14,
                            36,
                            27,
                            tzinfo=timezone.utc,
                        ),
                        status=EventStateStatus.CREATED,
                        comment_id=None,
                        other=None,
                        reason=None,
                    ),
                    type=EventType.MISSING_SUPPLIES,
                    root_id=None,
                    unreliable_indicators=EventUnreliableIndicators(
                        unreliable_solving_date=None
                    ),
                ),
            ]
        ],
    ],
)
@freeze_time("2022-12-05T06:00:00.0")
def test_get_open_events(
    *,
    events: list[Event],
) -> None:
    assert len(get_open_events(events)) == 3


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
