# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_stakeholder_organization_access')
async def test_admin(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    stakeholder_email: str = 'test1@gmail.com'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        org=org_id,
        stakeholder=stakeholder_email
    )
    assert 'errors' not in result
    assert result['data']['removeStakeholderOrganizationAccess']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_stakeholder_organization_access')
async def test_analyst(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    stakeholder_email: str = 'test2@gmail.com'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        org=org_id,
        stakeholder=stakeholder_email
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
