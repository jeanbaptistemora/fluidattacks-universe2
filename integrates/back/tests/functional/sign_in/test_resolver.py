# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('sign_in')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['signIn']
    assert not result['data']['signIn']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('sign_in')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['signIn']
    assert not result['data']['signIn']['success']
