# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('submit_draft')
async def test_admin(populate: bool):
    assert populate
    finding_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding=finding_id
    )
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('submit_draft')
async def test_analyst(populate: bool):
    assert populate
    finding_id: str = '475041514'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding=finding_id
    )
    assert 'errors' not in result
    assert result['data']['submitDraft']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('submit_draft')
async def test_analyst(populate: bool):
    assert populate
    finding_id: str = '475041515'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        finding=finding_id
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
