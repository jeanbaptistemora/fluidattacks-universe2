# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('unsubscribe_from_group')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
        ['executive@gmail.com'],
        ['resourcer@gmail.com'],
    ]
)
async def test_unsubscribe_from_group(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group='group1',
    )
    assert 'errors' not in result
    assert result['data']['unsubscribeFromGroup']['success']
