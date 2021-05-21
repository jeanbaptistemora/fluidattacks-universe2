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
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
        ['customer@gmail.com'],
    ]
)
async def test_download_event_file(populate: bool, email: str):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user=email,
        event=event_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']
