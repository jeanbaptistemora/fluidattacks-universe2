# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "events": [
            {
                "event": Event(
                    id="418900971",
                    group_name="group1",
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    description="ASM unit test1",
                    type=EventType.OTHER,
                    event_date="2018-06-27T12:00:00+00:00",
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name="evidence1",
                            modified_date="2019-03-11T15:57:45+00:00",
                        ),
                        file_1=EventEvidence(
                            file_name="1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                            modified_date="2019-03-11T15:57:45+00:00",
                        ),
                    ),
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2018-06-27T12:00:00+00:00",
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2018-06-27T19:40:05+00:00",
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900980",
                    group_name="group1",
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    description="ASM unit test2",
                    type=EventType.OTHER,
                    event_date="2018-06-27T12:00:00+00:00",
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name="evidence2",
                            modified_date="2019-03-11T15:57:45+00:00",
                        ),
                        file_1=EventEvidence(
                            file_name="1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                            modified_date="2019-03-11T15:57:45+00:00",
                        ),
                    ),
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2018-06-27T12:00:00+00:00",
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2018-06-27T19:40:05+00:00",
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
