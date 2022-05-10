# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [
                    "admin@gmail.com",
                    "hacker@gmail.com",
                    "reattacker@gmail.com",
                    "user@gmail.com",
                    "user_manager@gmail.com",
                    "vulnerability_manager@gmail.com",
                    "executive@gmail.com",
                    "customer_manager@fluidattacks.com",
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
                    "vulnerability_grace_period": 5,
                    "historic_max_number_acceptations": [
                        {
                            "date": "2019-11-22 15:07:57",
                            "user": "test1@gmail.com",
                            "max_number_acceptations": 4,
                        },
                    ],
                },
            },
            {
                "name": "acme",
                "id": "8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                "users": [
                    "admin@gmail.com",
                ],
                "groups": [
                    "group2",
                ],
                "policy": {},
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
