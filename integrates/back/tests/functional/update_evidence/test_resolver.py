# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_update_evidence(populate: bool, email: str):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidence']
    assert result['data']['updateEvidence']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence')
@pytest.mark.parametrize(
    ['email'],
    [
        ['executive@gmail.com'],
    ]
)
async def test_update_evidence_fail(populate: bool, email: str):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_id
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
