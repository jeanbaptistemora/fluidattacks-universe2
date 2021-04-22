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
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
    ]
)
async def test_edit_stakeholder(populate: bool, email: str):
    assert populate
    group_name: str = 'group1'
    phone_number: str = '123456'
    stakeholder_responsibility: str = 'Test'
    stakeholder_role: str = 'ADMIN'
    result: Dict[str, Any] = await query(
        user=email,
        stakeholder=email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('edit_stakeholder')
@pytest.mark.parametrize(
    ['email'],
    [
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_edit_stakeholder(populate: bool, email: str):
    assert populate
    group_name: str = 'group1'
    phone_number: str = '123456'
    stakeholder_responsibility: str = 'Test'
    stakeholder_role: str = 'ADMIN'
    result: Dict[str, Any] = await query(
        user=email,
        stakeholder=email,
        phone=phone_number,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
