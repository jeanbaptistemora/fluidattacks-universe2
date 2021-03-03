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
async def populate() -> bool:
    data: Dict[str, Any] = {
        'names': [
            {
                'entity': 'ORGANIZATION',
                'name': 'TESTORG',
            },
        ],
        'users': [
            {
                'email': 'test1@test1.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
        ],
        'policies': [
            {
                'level': 'user',
                'subject': 'test1@test1.com',
                'object': 'self',
                'role': 'admin',
            },
        ]
    }
    return await db.populate(data)
