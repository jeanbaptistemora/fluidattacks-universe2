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
@pytest.mark.resolver_test_group('edit_stakeholder_organization')
async def test_admin(populate: bool):
    assert populate
    context = get_new_context()
    admin: str = 'test1@gmail.com'
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    email: str = 'test2@gmail.com'
    role: str = 'CUSTOMER'
    phone: str = '12345678'
    query = f'''
        mutation {{
            editStakeholderOrganization(
                organizationId: "{org_id}",
                userEmail: "{email}",
                phoneNumber: "{phone}",
                role: {role}
            ) {{
                success
                modifiedStakeholder {{
                    email
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_graphql_result(
        data,
        stakeholder=admin,
        context=context,
    )
    assert 'errors' not in result
    assert result['data']['editStakeholderOrganization']['success']
    assert result['data']['editStakeholderOrganization']['modifiedStakeholder']['email'] == email
