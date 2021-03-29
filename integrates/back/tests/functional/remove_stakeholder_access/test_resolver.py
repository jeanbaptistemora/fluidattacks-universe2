# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_stakeholder_access')
async def test_admin(populate: bool):
    assert populate
    stakeholder_email: str = 'analyst@gmail.com'
    group_name: str = 'group-1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['removeStakeholderAccess']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_stakeholder_access')
async def test_analyst(populate: bool):
    assert populate
    stakeholder_email: str = 'analyst@gmail.com'
    group_name: str = 'group-1'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert 'errors' in result
    assert  result['errors'][0]['message'] == 'Access denied'
