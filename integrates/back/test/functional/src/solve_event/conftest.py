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
@pytest.mark.resolver_test_group("solve_event")
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
            {
                "event": Event(
                    id="418900972",
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
            {
                "event": Event(
                    id="418900973",
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
            {
                "event": Event(
                    id="418900974",
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
            {
                "event": Event(
                    id="418900975",
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
