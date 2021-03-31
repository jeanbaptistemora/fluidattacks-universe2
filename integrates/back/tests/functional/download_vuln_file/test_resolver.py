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
@pytest.mark.resolver_test_group('download_vuln_file')
async def test_admin(populate: bool):
    assert populate
    group: str = 'group1'
    finding_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        finding=finding_id
    )
    assert 'errors' not in result
    assert result['data']['downloadVulnFile']['success']
    assert 'url' in result['data']['downloadVulnFile']
    assert f'localhost:9000/fluidintegrates.reports/{group}-{finding_id}' \
        in result['data']['downloadVulnFile']['url']

@pytest.mark.asyncio
@pytest.mark.resolver_test_group('download_vuln_file')
async def test_analyst(populate: bool):
    assert populate
    group: str = 'group1'
    finding_id: str = '475041513'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        finding=finding_id
    )
    assert 'errors' not in result
    assert result['data']['downloadVulnFile']['success']
    assert 'url' in result['data']['downloadVulnFile']
    assert f'localhost:9000/fluidintegrates.reports/{group}-{finding_id}' \
        in result['data']['downloadVulnFile']['url']
