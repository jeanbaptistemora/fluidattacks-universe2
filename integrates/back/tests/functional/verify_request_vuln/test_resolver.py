# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('verify_request_vuln')
async def test_admin(populate: bool):
    assert populate
    finding_id: str = '475041513'
    vulnerability_id: str = 'be09edb7-cd5c-47ed-bee4-97c645acdce8'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding=finding_id,
        vulnerability=vulnerability_id
    )
    assert 'errors' not in result
    assert result['data']['verifyRequestVuln']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('verify_request_vuln')
async def test_analyst(populate: bool):
    assert populate
    finding_id: str = '475041513'
    vulnerability_id: str = 'be09edb7-cd5c-47ed-bee4-97c645acdce9'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding=finding_id,
        vulnerability=vulnerability_id
    )
    assert 'errors' not in result
    assert result['data']['verifyRequestVuln']['success']