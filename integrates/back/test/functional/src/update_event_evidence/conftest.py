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
                "analyst": "unittest@fluidattacks.com",
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
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
                "subscription": "ONESHOT",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
