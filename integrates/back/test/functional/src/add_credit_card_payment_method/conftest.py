from back.test import (  # pylint: disable=import-error
    db,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("add_credit_card_payment_method")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    return await db.populate({**generic_data["db_data"]})
