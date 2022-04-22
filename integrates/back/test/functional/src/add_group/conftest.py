# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "names": [
            {
                "entity": "GROUP",
                "name": "GROUP1",
            },
        ],
        "orgs": [
            {
                "name": "orgtest",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [],
                "groups": [
                    "group2",
                    "group3",
                ],
                "policy": {},
            },
        ],
        "groups": [
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
            {
                "project_name": "group3",
                "description": "-",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": True,
                        "requester": "unknown",
                        "service": "BLACK",
                        "type": "oneshot",
                    }
                ],
                "project_status": "DELETED",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
