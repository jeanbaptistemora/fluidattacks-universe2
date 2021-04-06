# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_group')
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group=group_name
    )
    assert 'errors' not in result
    assert result['data']['removeGroup']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_group')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group2'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group=group_name
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
