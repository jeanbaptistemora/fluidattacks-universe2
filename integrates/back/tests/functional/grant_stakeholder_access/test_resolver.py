# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('grant_stakeholder_access')
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group-1'
    stakeholder_email: str = 'analyst@gmail.com'
    phone_number: str = '-'
    stakeholder_responsibility: str = 'test'
    stakeholder_role: str = 'EXECUTIVE'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        stakeholder=stakeholder_email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' not in result
    assert result['data']['grantStakeholderAccess']['success']
    assert result['data']['grantStakeholderAccess']['grantedStakeholder']['email'] == stakeholder_email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('grant_stakeholder_access')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group-1'
    stakeholder_email: str = 'analyst@gmail.com'
    phone_number: str = '-'
    stakeholder_responsibility: str = 'test'
    stakeholder_role: str = 'EXECUTIVE'
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



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('grant_stakeholder_access')
async def test_closer(populate: bool):
    assert populate
    group_name: str = 'group-1'
    stakeholder_email: str = 'analyst@gmail.com'
    phone_number: str = '-'
    stakeholder_responsibility: str = 'test'
    stakeholder_role: str = 'EXECUTIVE'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        stakeholder=stakeholder_email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
