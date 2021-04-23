# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('stakeholder')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
    ]
)
async def test_get_stakeholder(populate: bool, email: str):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user=email,
        stakeholder=email,
        group=group_name,
    )
    assert 'errors' not in result
    assert result['data']['stakeholder']['email'] == email
    assert result['data']['stakeholder']['role'] == email.split("@")[0]
    assert result['data']['stakeholder']['responsibility'] == ''
    assert result['data']['stakeholder']['phoneNumber'] == '-'
    assert result['data']['stakeholder']['firstLogin'] == ''
    assert result['data']['stakeholder']['lastLogin'] == ''


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('stakeholder')
@pytest.mark.parametrize(
    ['email'],
    [
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_get_stakeholder_fail(populate: bool, email: str):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user=email,
        stakeholder=email,
        group=group_name,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
