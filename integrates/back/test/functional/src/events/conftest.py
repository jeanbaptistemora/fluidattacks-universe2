# pylint: disable=import-error
from back.test import (
    db,
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
                "group_name": "group1",
                "event_id": "418900971",
                "accessibility": "Repositorio",
                "affected_components": "affected_components_test",
                "analyst": "unittest@fluidattacks.com",
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 14:40:05",
                "context": "FLUID",
                "detail": "ASM unit test1",
                "historic_state": [
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 14:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "hours_before_blocking": "1",
                "subscription": "ONESHOT",
                "evidence": "evidence1",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:45",
            },
            {
                "project_name": "group1",
                "event_id": "418900980",
                "accessibility": "Repositorio",
                "affected_components": "affected_components_test",
                "analyst": "unittest@fluidattacks.com",
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 14:40:05",
                "context": "FLUID",
                "detail": "ASM unit test2",
                "historic_state": [
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 14:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "hours_before_blocking": "1",
                "subscription": "ONESHOT",
                "evidence": "evidence2",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:45",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
