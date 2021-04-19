# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('groups_with_forces')
async def test_admin(populate: bool):
    assert populate
    group_forces: str = 'group2'
    group_not_forces: str = 'group1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
    )
    assert 'errors' not in result
    assert group_forces in result['data']['groupsWithForces']
    assert group_not_forces not in result['data']['groupsWithForces']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('groups_with_forces')
async def test_analyst(populate: bool):
    assert populate
    group_forces: str = 'group2'
    group_not_forces: str = 'group1'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
