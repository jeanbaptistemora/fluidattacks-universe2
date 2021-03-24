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
@pytest.mark.resolver_test_group('forces_executions')
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
            },
        ],
        'executions' : [
            {
                'project_name' : 'group-1',
                'execution_id' : '123',
                'date' : '2020-02-05T00:00:00Z',
                'exit_code' : '1',
                'git_branch' : 'master',
                'git_commit' : '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6',
                'git_origin' : 'http://test.com',
                'git_repo' : 'Repository',
                'kind' : 'dynamic',
                'strictness': 'strict',
                'vulnerabilities': {
                    'num_of_accepted_vulnerabilities': 1,
                    'num_of_open_vulnerabilities': 1,
                    'num_of_closed_vulnerabilities': 1,
                },
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
