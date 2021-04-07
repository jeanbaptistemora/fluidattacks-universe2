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
async def test_admin(populate: bool):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidence']
    assert result['data']['updateEvidence']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence')
async def test_analyst(populate: bool):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidence']
    assert result['data']['updateEvidence']['success']
