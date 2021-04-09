# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_severity')
async def test_admin(populate: bool):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateSeverity']
    assert result['data']['updateSeverity']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_severity')
async def test_analyst(populate: bool):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateSeverity']
    assert result['data']['updateSeverity']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_severity')
async def test_closer(populate: bool):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        draft=draft_id
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
