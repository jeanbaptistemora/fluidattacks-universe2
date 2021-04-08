# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_event_file')
async def test_admin(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        event=event_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_event_file')
async def test_analyst(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        event=event_id

    )
    assert 'errors' not in result
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']
