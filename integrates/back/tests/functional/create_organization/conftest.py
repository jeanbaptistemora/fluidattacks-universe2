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
@pytest.mark.resolver_test_group('create_organization')
@pytest.fixture(autouse=True, scope='session')
async def populate(get_generic_data: Dict[str, Any]) -> bool:
    generic_data: Dict[str, Any] = get_generic_data
    data: Dict[str, Any] = {
        'names': [
            {
                'entity': 'ORGANIZATION',
                'name': 'TESTORG',
            },
        ],
        'orgs': [],
        'groups': [],
    }
    return await db.populate({**generic_data, **data})
