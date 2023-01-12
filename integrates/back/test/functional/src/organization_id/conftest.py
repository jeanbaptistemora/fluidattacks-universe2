# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Dict,
)


@pytest.mark.resolver_test_group("organization_id")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    return await db.populate(generic_data["db_data"])
