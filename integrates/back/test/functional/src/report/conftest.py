# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "project_name": "group1",
                "description": "This is a dummy description",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
                "business_id": "123",
                "business_name": "acme",
            },
            {
                "project_name": "group2",
                "description": "-",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": True,
                        "has_forces": True,
                        "requester": "unknown",
                        "service": "BLACK",
                        "type": "oneshot",
                    }
                ],
                "project_status": "ACTIVE",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
