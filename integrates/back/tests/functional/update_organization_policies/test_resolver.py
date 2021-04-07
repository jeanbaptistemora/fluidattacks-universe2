# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_organization_policies')
async def test_admin(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        id=org_id,
        name=org_name,
    )
    assert 'errors' not in result
    assert result['data']['updateOrganizationPolicies']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_organization_policies')
async def test_analyst(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        id=org_id,
        name=org_name,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
