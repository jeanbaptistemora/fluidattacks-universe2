# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_files')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group='group-1',
    )
    assert 'errors' not in result
    assert result['data']['removeFiles']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_files')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group='group-1',
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
