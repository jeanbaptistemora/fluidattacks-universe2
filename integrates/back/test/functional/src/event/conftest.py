# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.events.enums import (
    EventAccessibility,
    EventAffectedComponents,
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
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("event")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "events": [
            {
                "event": Event(
                    id="418900971",
                    group_name="group1",
                    accessibility={EventAccessibility.REPOSITORY},
                    affected_components={
                        EventAffectedComponents.FLUID_STATION
                    },
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    description="ASM unit test",
                    type=EventType.OTHER,
                    event_date="2018-06-27T12:00:00+00:00",
                    evidences=EventEvidences(
                        image=EventEvidence(
                            file_name="1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                            modified_date="2019-03-11T15:57:45+00:00",
                        ),
                        file=EventEvidence(
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
        "comments": [
            {
                "finding_id": "418900971",
                "comment_id": "43455343453",
                "comment_type": "event",
                "content": "This is a test comment",
                "created": "2019-05-28 15:09:37",
                "email": "admin@gmail.com",
                "fullname": "test one",
                "modified": "2019-05-28 15:09:37",
                "parent": 0,
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
