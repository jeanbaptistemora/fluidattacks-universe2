# Standard libraries
from typing import (
    Any,
    Dict,
)

# Third party libraries
import pytest

# Local libraries
from back.tests import (
    db,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('organization_id')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
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
        'orgs': [
            {
                'name': 'orgtest',
                'users': [
                    'test1@test1.com',
                ],
            },
        ],
        'policies': [
            {
                'level': 'user',
                'subject': 'test1@test1.com',
                'object': 'self',
                'role': 'admin',
            },
            {
                'level': 'organization',
                'subject': 'test1@test1.com',
                'object': 'orgtest',
                'role': 'customeradmin',
            },
        ]
    }
    return await db.populate(data)
