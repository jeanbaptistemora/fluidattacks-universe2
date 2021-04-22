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
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
    ]
)
async def test_approve_draft(populate: bool, email: str):
    assert populate
    draft_name: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_name,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['approveDraft']
    assert result['data']['approveDraft']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('approve_draft')
@pytest.mark.parametrize(
    ['email'],
    [
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_approve_draft_fail(populate: bool, email: str):
    assert populate
    draft_name: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_name,
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
