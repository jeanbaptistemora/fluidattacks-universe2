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
@pytest.mark.resolver_test_group('remove_files')
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
        ],
        'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [
                    'admin@gmail.com',
                    'analyst@gmail.com',
                ],
                'groups': [
                    'group-1',
                ],
                'policy': {},
            },
        ],
        'groups': [
            {
                'project_name': 'group-1',
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
                'files': [
                    {
                        'description': 'Test',
                        'fileName': 'test.zip',
                        'uploadDate': '2019-03-01 15:21',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'fileName': 'shell.exe',
                        'uploadDate': '2019-04-24 14:56',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'fileName': 'shell2.exe',
                        'uploadDate': '2019-04-24 14:59',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'fileName': 'asdasd.py',
                        'uploadDate': '2019-08-06 14:28',
                        'uploader': 'unittest@fluidattacks.com',
                    },
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
                'object': 'group-1',
                'role': 'analyst',
            },
            {
                'level': 'organization',
                'subject': 'analyst@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customer',
            },
        ],
    }
    return await db.populate(data)
