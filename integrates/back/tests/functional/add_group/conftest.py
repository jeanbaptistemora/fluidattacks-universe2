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
@pytest.mark.resolver_test_group("add_group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
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
                "groups": [],
                "policy": {},
            },
        ],
        "groups": [],
    }
    return await db.populate({**generic_data["db_data"], **data})
