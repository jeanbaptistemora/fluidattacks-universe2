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
@pytest.mark.resolver_test_group('remove_tag')
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
                'email': 'closer@gmail.com',
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
                    'test1@gmail.com',
                ],
                'groups': [
                    'group1',
                ],
                'policy': {},
            },
        ],
        'groups': [
            {
                'project_name': 'group1',
                'description': '-',
                'language': 'en',
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': False,
                    'has_forces': False,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
                'tag': [
                    'test1',
                    'test2',
                ],
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
            {
                'level': 'user',
                'subject': 'closer@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'group',
                'subject': 'closer@gmail.com',
                'object': 'group1',
                'role': 'closer',
            },
        ],
    }
    return await db.populate(data)
