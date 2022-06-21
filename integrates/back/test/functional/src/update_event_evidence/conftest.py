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
    EventEvidences,
    EventState,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_evidence")
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
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    description="ASM unit test",
                    type=EventType.OTHER,
                    event_date="2018-06-27T12:00:00+00:00",
                    evidences=EventEvidences(image=None, file=None),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date="2018-06-27T12:00:00+00:00",
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date="2018-06-27T19:40:05+00:00",
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
