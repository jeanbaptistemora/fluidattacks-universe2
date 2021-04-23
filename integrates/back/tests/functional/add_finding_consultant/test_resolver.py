# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('add_finding_consult')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_add_finding_consultant(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        content='This is a observation test',
        finding='475041513',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['addFindingConsult']
    assert result['data']['addFindingConsult']['success']
