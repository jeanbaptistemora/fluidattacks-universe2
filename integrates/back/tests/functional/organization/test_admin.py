# Standard libraries
import pytest
from typing import (
    List,
)

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)
from backend.exceptions import (
    UserNotInOrganization,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('organization')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    user: str = 'test2@gmail.com'
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    org_groups: List[str] = [
        'group1',
        'group2',
    ]
    org_stakeholders: List[str] = [
        'test1@gmail.com',
        'test2@gmail.com',
    ]
    query = f'''
        query {{
            organization(organizationId: "{org_id}") {{
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptations
                minAcceptanceSeverity
                name
                projects {{
                    name
                }}
                stakeholders {{
                    email
                }}
            }}
        }}
    '''
    # Admin
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    groups = [group['name'] for group in result['data']['organization']['projects']]
    stakeholders = [stakeholder['email'] for stakeholder in result['data']['organization']['stakeholders']]
    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == 90
    assert result['data']['organization']['maxAcceptanceSeverity'] == 7
    assert result['data']['organization']['maxNumberAcceptations'] == 4
    assert result['data']['organization']['minAcceptanceSeverity'] == 3
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == org_groups
    assert sorted(stakeholders) == org_stakeholders

    # Stakeholder
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    groups = [group['name'] for group in result['data']['organization']['projects']]
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == 90
    assert result['data']['organization']['maxAcceptanceSeverity'] == 7
    assert result['data']['organization']['maxNumberAcceptations'] == 4
    assert result['data']['organization']['minAcceptanceSeverity'] == 3
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == org_groups

    # Made up user
    exe = UserNotInOrganization()
    result = await get_graphql_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
