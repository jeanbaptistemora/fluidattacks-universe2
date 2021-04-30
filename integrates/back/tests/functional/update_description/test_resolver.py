# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_finding_description')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_update_finding_description(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateDescription']
    assert result['data']['updateDescription']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_finding_description')
@pytest.mark.parametrize(
    ['email'],
    [
        ['executive@gmail.com'],
    ]
)
async def test_update_finding_description_fail(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
