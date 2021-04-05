# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('grant_stakeholder_organization_access')
async def test_admin(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    admin: str = 'test1@gmail.com'
    stakeholder_email: str = 'test2@gmail.com'
    stakeholder_role: str = 'CUSTOMER'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        org=org_id,
        role=stakeholder_role,
        email=stakeholder_email
    )
    assert 'errors' not in result
    assert result['data']['grantStakeholderOrganizationAccess']['success']
    assert result['data']['grantStakeholderOrganizationAccess']['grantedStakeholder']['email'] == stakeholder_email



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('grant_stakeholder_organization_access')
async def test_analyst(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    admin: str = 'test1@gmail.com'
    stakeholder_email: str = 'test2@gmail.com'
    stakeholder_role: str = 'CUSTOMER'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        org=org_id,
        role=stakeholder_role,
        email=stakeholder_email
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
