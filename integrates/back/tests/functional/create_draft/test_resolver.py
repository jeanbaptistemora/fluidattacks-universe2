# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_draft')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['createDraft']
    assert result['data']['createDraft']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_draft')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
    )
    assert 'errors' not in result
    assert 'success' in result['data']['createDraft']
    assert result['data']['createDraft']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('create_draft')
async def test_closer(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
