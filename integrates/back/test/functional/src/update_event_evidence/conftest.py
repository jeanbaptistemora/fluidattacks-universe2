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
@pytest.mark.resolver_test_group("update_event_evidence")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "events": [
            {
                "project_name": "group1",
                "event_id": "418900971",
                "accessibility": "Repositorio",
                "action_after_blocking": "EXECUTE_OTHER_GROUP_SAME_CLIENT",
                "action_before_blocking": "TEST_OTHER_PART_TOE",
                "analyst": "unittest@fluidattacks.com",
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "context": "FLUID",
                "detail": "ASM unit test",
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
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
