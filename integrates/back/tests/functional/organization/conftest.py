from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [
                    "admin@gmail.com",
                    "hacker@gmail.com",
                    "reattacker@gmail.com",
                    "customer@gmail.com",
                    "customeradmin@gmail.com",
                    "executive@gmail.com",
                    "system_owner@gmail.com",
                    "resourcer@gmail.com",
                    "reviewer@gmail.com",
                ],
                "groups": [
                    "group1",
                ],
                "policy": {
                    "max_acceptance_days": 90,
                    "max_number_acceptations": 4,
                    "max_acceptance_severity": 7,
                    "min_acceptance_severity": 3,
                    "min_breaking_severity": 2,
                    "historic_max_number_acceptations": [
                        {
                            "date": "2019-11-22 15:07:57",
                            "user": "test1@gmail.com",
                            "max_number_acceptations": 4,
                        },
                    ],
                },
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
