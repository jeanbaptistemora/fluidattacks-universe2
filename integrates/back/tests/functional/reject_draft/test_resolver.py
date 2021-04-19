# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('reject_draft')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        draft='475041513',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['rejectDraft']
    assert result['data']['rejectDraft']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('reject_draft')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        draft='475041520',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['rejectDraft']
    assert result['data']['rejectDraft']['success']
