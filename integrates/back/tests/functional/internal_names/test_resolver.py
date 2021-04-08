# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('internal_names')
async def test_admin(populate: bool):
    assert populate
    group: str = 'group1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
    )
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    assert result['data']['internalNames']['name'] == group



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('internal_names')
async def test_analyst(populate: bool):
    assert populate
    group: str = 'group1'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
