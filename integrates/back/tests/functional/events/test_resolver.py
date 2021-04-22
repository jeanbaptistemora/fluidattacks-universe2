# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('events')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_get_events(populate: bool, email: str):
    assert populate
    expected: List[Dict[str, str]] = [
        {
            'id': '418900971',
            'projectName': 'group1',
            'eventStatus': 'CREATED',
            'evidence': 'evidence1',
            'detail': 'Integrates unit test1',
        },
        {
            'id': '418900980',
            'projectName': 'group1',
            'eventStatus': 'CREATED',
            'evidence': 'evidence2',
            'detail': 'Integrates unit test2',
        },
    ]
    group_name: str = 'group1'
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name
    )
    assert 'errors' not in result
    assert result['data']['events'] == expected
