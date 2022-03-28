# pylint: disable=import-error
from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_tags")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    return await db.populate(generic_data["db_data"])
