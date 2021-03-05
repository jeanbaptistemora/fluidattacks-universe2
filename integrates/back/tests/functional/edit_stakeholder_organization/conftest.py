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
@pytest.mark.resolver_test_group('edit_stakeholder_organization')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
        'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [
                    'test1@gmail.com',
                    'test2@gmail.com',
                ],
                'groups': [],
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
            {
                'email': 'test2@gmail.com',
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
            {
                'level': 'organization',
                'subject': 'test1@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customeradmin',
            },
            {
                'level': 'user',
                'subject': 'test2@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'organization',
                'subject': 'test2@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customer',
            },
        ],
    }
    return await db.populate(data)
