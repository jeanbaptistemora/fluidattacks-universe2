# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_finding_description')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com'
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateDescription']
    assert result['data']['updateDescription']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_finding_description')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com'
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateDescription']
    assert result['data']['updateDescription']['success']
