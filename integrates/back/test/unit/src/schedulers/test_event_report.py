from datetime import (
    datetime,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidences,
    EventState,
)
from freezegun import (
    freeze_time,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from schedulers.event_report import (
    days_to_date,
    send_event_report,
)
from unittest import (
    mock,
)


@freeze_time("2022-09-19")
def test_days_to_date() -> None:
    date = datetime.fromisoformat("2022-09-10T00:00:00+00:00")
    days = days_to_date(date)
    assert days == 9


@freeze_time("2022-09-19")
@pytest.mark.asyncio
async def test_send_event_report() -> None:
    new_event = Event(
        client="c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        created_by="unittesting@fluidattacks.com",
        created_date=datetime_utils.get_iso_date(),
        description="Something happened.",
        event_date="2022-09-10T00:00:00+00:00",
        evidences=EventEvidences(),
        group_name="unittesting",
        hacker="unittesting@fluidattacks.com",
        id="11111111",
        state=EventState(
            modified_by="unittesting@fluidattacks.com",
            modified_date=datetime.fromisoformat("2022-09-10T00:00:00+00:00"),
            status=EventStateStatus.CREATED,
        ),
        type=EventType["AUTHORIZATION_SPECIAL_ATTACK"],
    )
    unsolved_events_mock = [new_event]
    with mock.patch(
        "schedulers.event_report.events_domain.get_unsolved_events",
        coroutine=unsolved_events_mock,
    ) as mock_event:
        await send_event_report()
        assert mock_event.called is True
