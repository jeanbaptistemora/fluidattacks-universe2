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
@pytest.mark.resolver_test_group('remove_stakeholder_organization_access')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
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
        'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [
                    'admin@gmail.com',
                    'analyst@gmail.com',
                    'test1@gmail.com',
                    'test2@gmail.com',
                ],
                'groups': [],
                'policy': {},
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
                'level': 'user',
                'subject': 'test1@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'user',
                'subject': 'test2@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'organization',
                'subject': 'analyst@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customer',
            },
            {
                'level': 'organization',
                'subject': 'test1@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customer',
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
