# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_event_evidence')
async def test_admin(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        event=event_id
    )
    assert result['data']['removeEventEvidence']['success'] 



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_event_evidence')
async def test_analyst(populate: bool):
    assert populate
    event_id: str = '418900980'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        event=event_id
    )
    assert result['data']['removeEventEvidence']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_event_evidence')
async def test_analyst(populate: bool):
    assert populate
    event_id: str = '418900995'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        event=event_id
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
