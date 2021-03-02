# Third party libraries
import pytest

# Local libraries
from back.tests.functional.utils import (
    get_graphql_result,
)
from back.tests.functional.populate import (
    populate_db,
    clean_db,
)


@pytest.mark.asyncio
@pytest.mark.stateless
async def test_organization_admin():
    data = {
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
    assert await populate_db(data)
    query = '''{
        organizationId(organizationName: "orgtest") {
            id
        }
    }'''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        'test1@test1.com',
    )
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] != None
    assert await clean_db()
