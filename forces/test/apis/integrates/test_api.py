# Third party libraries
import pytest

# Local libraries
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
    get_vulnerabilities,
    vulns_generator
)


@pytest.mark.asyncio  # type: ignore
async def test_get_findings(
    test_group: str,
    test_token: str,
    test_finding: str
) -> None:
    result = await get_findings(test_group, api_token=test_token)
    assert test_finding in result


@pytest.mark.asyncio  # type: ignore
async def test_get_finding(
    test_token: str,
    test_finding: str
)-> None:
    result = await get_finding(test_finding, api_token=test_token)
    assert result['id'] == test_finding


@pytest.mark.asyncio  # type: ignore
async def test_get_vulnerabilities(test_token: str, test_finding: str) -> None:
    result = await get_vulnerabilities(test_finding, api_token=test_token)
    assert len(result) == 5
    for vuln in result:
        assert 'forces' in vuln['where']


@pytest.mark.asyncio  # type: ignore
async def test_vulns_generator(test_token: str, test_group: str) -> None:
    vulns = [vuln async for vuln in vulns_generator(test_group, api_token=test_token)]
    assert len(vulns) == 5
