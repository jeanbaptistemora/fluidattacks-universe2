# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('approve_draft')
async def test_admin(populate: bool):
    assert populate
    group_name: str = 'group-1'
    draft_name: str = '475041513'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        draft=draft_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['approveDraft']
    assert result['data']['approveDraft']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('approve_draft')
async def test_analyst(populate: bool):
    assert populate
    group_name: str = 'group-1'
    draft_name: str = '475041513'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        draft=draft_name,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('approve_draft')
async def test_closer(populate: bool):
    assert populate
    group_name: str = 'group-1'
    draft_name: str = '475041513'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        draft=draft_name,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
