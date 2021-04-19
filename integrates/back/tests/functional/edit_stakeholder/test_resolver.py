# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('edit_stakeholder')
async def test_admin(populate: bool):
    assert populate
    stakeholder_email: str = 'analyst@gmail.com'
    group_name: str = 'group1'
    phone_number: str = '123456'
    stakeholder_responsibility: str = 'Test'
    stakeholder_role: str = 'ADMIN'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        stakeholder=stakeholder_email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('edit_stakeholder')
async def test_analyst(populate: bool):
    assert populate
    stakeholder_email: str = 'analyst@gmail.com'
    group_name: str = 'group1'
    phone_number: str = '123456'
    stakeholder_responsibility: str = 'Test'
    stakeholder_role: str = 'ADMIN'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        stakeholder=stakeholder_email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
