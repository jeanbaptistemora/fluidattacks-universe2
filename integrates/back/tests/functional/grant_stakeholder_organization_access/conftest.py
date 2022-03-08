# pylint: disable=import-error
from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_organization_access")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest2",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6dc",
                "users": [],
                "groups": [],
                "policy": {},
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
