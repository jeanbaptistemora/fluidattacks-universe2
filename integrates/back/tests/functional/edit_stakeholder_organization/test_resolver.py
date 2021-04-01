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
@pytest.mark.resolver_test_group('edit_stakeholder_organization')
async def test_admin(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    user_email: str = 'analyst@gmail.com'
    user_role: str = 'CUSTOMER'
    user_phone: str = '12345678'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        org=org_id,
        email=user_email,
        role=user_role,
        phone=user_phone,
    )
    assert 'errors' not in result
    assert result['data']['editStakeholderOrganization']['success']
    assert result['data']['editStakeholderOrganization']['modifiedStakeholder']['email'] == user_email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('edit_stakeholder_organization')
async def test_analyst(populate: bool):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    user_email: str = 'analyst@gmail.com'
    user_role: str = 'CUSTOMER'
    user_phone: str = '12345678'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        org=org_id,
        email=user_email,
        role=user_role,
        phone=user_phone,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
