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
@pytest.mark.resolver_test_group('groups_with_forces')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
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
        'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [
                    'test1@gmail.com',
                ],
                'groups': [
                    'group-1',
                    'group-2',
                ],
                'policy': {},
            },
        ],
        'groups': [
            {
                'project_name': 'group-1',
                'description': '-',
                'language': 'en',
                'comments': [],
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': False,
                    'has_forces': False,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
            },
            {
                'project_name': 'group-2',
                'description': '-',
                'language': 'en',
                'comments': [],
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': False,
                    'has_forces': True,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
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
