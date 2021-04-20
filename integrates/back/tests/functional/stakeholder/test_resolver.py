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
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group1'
    stakeholder_email: str = 'analyst@gmail.com'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        stakeholder=stakeholder_email,
        group=group_name,
    )
    assert 'errors' not in result
    assert result['data']['stakeholder']['email'] == stakeholder_email
    assert result['data']['stakeholder']['role'] == 'analyst'
    assert result['data']['stakeholder']['responsibility'] == ''
    assert result['data']['stakeholder']['phoneNumber'] == '-'
    assert result['data']['stakeholder']['firstLogin'] == ''
    assert result['data']['stakeholder']['lastLogin'] == ''
    assert result['data']['stakeholder']['projects'] == [{'name': 'group1'}]
    


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('stakeholder')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group1'
    stakeholder_email: str = 'analyst@gmail.com'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        stakeholder=stakeholder_email,
        group=group_name,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
