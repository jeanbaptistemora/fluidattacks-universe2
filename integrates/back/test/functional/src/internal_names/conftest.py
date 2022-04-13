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
@pytest.mark.resolver_test_group("internal_names")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "names": [
            {
                "entity": "GROUP",
                "name": "GROUP1",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
