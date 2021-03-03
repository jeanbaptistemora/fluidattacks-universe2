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
@pytest.mark.resolver_test_group('grant_stakeholder_organization_access')
async def test_admin(populate: bool):
    context = get_new_context()
    assert populate
    org_id = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    admin = 'test1@gmail.com'
    stakeholder = 'test2@gmail.com'
    stakeholder_role = 'CUSTOMER'
    query = f'''
        mutation {{
            grantStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
            ) {{
                success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    '''

    # Make admin give access to stakeholder
    data = {'query': query}
    result = await get_graphql_result(
        data,
        admin,
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['grantStakeholderOrganizationAccess']['success']
    assert result['data']['grantStakeholderOrganizationAccess']['grantedStakeholder']['email'] == stakeholder

    # Make stakeholder give access to stakeholder
    result = await get_graphql_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    # Make non-existant user give access to stakeholder
    result = await get_graphql_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
