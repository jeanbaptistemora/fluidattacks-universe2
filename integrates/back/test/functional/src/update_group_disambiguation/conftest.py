# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("update_group_disambiguation")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict) -> bool:
    return await db.populate(generic_data["db_data"])
