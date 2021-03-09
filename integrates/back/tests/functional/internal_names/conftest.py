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
@pytest.mark.resolver_test_group('internal_names')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
        'names': [
            {
                'entity': 'GROUP',
                'name': 'GROUP1',
            },
        ],
        'users': [
            {
                'email': 'test1@gmail.com',
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
                'subject': 'test1@gmail.com',
                'object': 'self',
                'role': 'admin',
            },
        ],
    }
    return await db.populate(data)
