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
@pytest.mark.resolver_test_group('create_project')
async def test_admin(populate: bool):
    assert populate
    org_name: str = 'orgtest'
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        org=org_name,
        group=group_name
    )
    assert 'errors' not in result
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_project')
async def test_analyst(populate: bool):
    assert populate
    org_name: str = 'orgtest'
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        org=org_name,
        group=group_name
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
