# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_evidence')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding='475041513',
        evidence='EVIDENCE1',
    )
    assert 'errors' not in result
    assert result['data']['removeEvidence']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_evidence')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding='475041513',
        evidence='EVIDENCE2',
    )
    assert 'errors' not in result
    assert result['data']['removeEvidence']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('remove_evidence')
async def test_closer(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        finding='475041513',
        evidence='EVIDENCE3',
    )
    assert 'errors' not in result
    assert result['data']['removeEvidence']['success']
