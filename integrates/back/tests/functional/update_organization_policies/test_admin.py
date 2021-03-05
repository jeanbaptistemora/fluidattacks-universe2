# Standard libraries
import pytest

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)
from backend.exceptions import (
    UserNotInOrganization,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_organization_policies')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    user: str = 'test2@gmail.com'
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    query = f'''
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.5,
                maxNumberAcceptations: 3,
                minAcceptanceSeverity: 1.5,
                organizationId: "{org_id}",
                organizationName: "{org_name}"
            ) {{
                success
            }}
        }}
    '''

    # Update with admin
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['updateOrganizationPolicies']['success']

    # Update with non-privileged user
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=context,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    # Update with non-existing user
    result = await get_graphql_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
