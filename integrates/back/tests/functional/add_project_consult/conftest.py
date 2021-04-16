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
@pytest.mark.resolver_test_group('add_project_consult')
@pytest.fixture(autouse=True, scope='session')
async def populate(get_generic_data: Dict[str, Any]) -> bool:
    generic_data: Dict[str, Any] = get_generic_data
    return await db.populate(generic_data)
