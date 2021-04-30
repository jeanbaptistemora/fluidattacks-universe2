# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_severity')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
    ]
)
async def test_update_severity(populate: bool, email: str):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_id
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateSeverity']
    assert result['data']['updateSeverity']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_severity')
@pytest.mark.parametrize(
    ['email'],
    [
        ['closer@gmail.com'],
        ['executive@gmail.com'],
    ]
)
async def test_update_severity_fail(populate: bool, email: str):
    assert populate
    draft_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user=email,
        draft=draft_id
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
