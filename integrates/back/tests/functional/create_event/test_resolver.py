# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_event')
async def test_admin(populate: bool):
    assert populate
    admin: str ='admin@gmail.com'
    group_name: str ='group-1'
    result: Dict[str, str] = await query(
        user=admin,
        group=group_name,
    )
    assert 'errors' not in result
    assert result['data']['createEvent']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_event')
async def test_analyst(populate: bool):
    assert populate
    analyst: str ='analyst@gmail.com'
    group_name: str ='group-1'
    result: Dict[str, str] = await query(
        user=analyst,
        group=group_name,
    )
    assert 'errors' not in result
    assert result['data']['createEvent']
