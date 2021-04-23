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
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
    ]
)
async def test_admin(populate: bool, email: str):
    assert populate
    group: str = 'group1'
    result: Dict[str, Any] = await query(
        user=email,
    )
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    assert result['data']['internalNames']['name'] == group


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('internal_names')
@pytest.mark.parametrize(
    ['email'],
    [
        ['closer@gmail.com'],
    ]
)
async def test_closer(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
