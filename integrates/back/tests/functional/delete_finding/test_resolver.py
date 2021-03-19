# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('delete_finding')
async def test_admin(populate: bool):
    assert populate
    admin: str ='admin@gmail.com'
    finding_id: str = '475041513'
    result: Dict[str, str] = await query(
        user=admin,
        finding=finding_id,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['deleteFinding']
    assert result['data']['deleteFinding']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('delete_finding')
async def test_analyst(populate: bool):
    assert populate
    analyst: str ='analyst@gmail.com'
    finding_id: str = '475041514'
    result: Dict[str, str] = await query(
        user=analyst,
        finding=finding_id,
    )
    assert 'errors' not in result
    assert 'success' in result['data']['deleteFinding']
    assert result['data']['deleteFinding']['success']
