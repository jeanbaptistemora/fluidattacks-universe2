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
                'email': 'admin@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'analyst@gmail.com',
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
                'subject': 'admin@gmail.com',
                'object': 'self',
                'role': 'admin',
            },
            {
                'level': 'user',
                'subject': 'analyst@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'group',
                'subject': 'analyst@gmail.com',
                'object': 'group1',
                'role': 'analyst',
            },
        ]
    }
    return await db.populate(data)
