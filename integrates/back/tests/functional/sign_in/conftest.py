# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests import (
    db,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("sign_in")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    return await db.populate(generic_data["db_data"])
