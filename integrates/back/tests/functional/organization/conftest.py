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
@pytest.mark.resolver_test_group('organization')
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
                    'test1@gmail.com',
                    'test2@gmail.com',
                ],
                'groups': [
                    'group1',
                    'group2',
                ],
                'policy': {
                    'max_acceptance_days': 90,
                    'max_number_acceptations': 4,
                    'max_acceptance_severity': 7,
                    'min_acceptance_severity': 3,
                    'historic_max_number_acceptations': [
                        {
                            'date': '2019-11-22 15:07:57',
                            'user': 'test1@gmail.com',
                            'max_number_acceptations': 4,
                        },
                    ],
                },
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
            },
            {
                'project_name': 'group2',
                'description': '-',
                'language': 'en',
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
            {
                'level': 'group',
                'subject': 'test1@gmail.com',
                'object': 'group1',
                'role': 'customeradmin',
            },
            {
                'level': 'group',
                'subject': 'test1@gmail.com',
                'object': 'group2',
                'role': 'customeradmin',
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
                'level': 'group',
                'subject': 'test2@gmail.com',
                'object': 'group1',
                'role': 'customer',
            },
            {
                'level': 'group',
                'subject': 'test2@gmail.com',
                'object': 'group2',
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
