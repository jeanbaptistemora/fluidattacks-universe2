from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_findings,
    get_groups_access,
    get_vulnerabilities,
)
from forces.apis.integrates.client import (
    ApiError,
)
from forces.model import (
    ForcesConfig,
    KindEnum,
)
import pytest


@pytest.mark.asyncio
async def test_get_findings(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    result = await get_findings(test_group, api_token=test_token)
    assert test_finding in result[0]["id"]


@pytest.mark.asyncio
async def test_get_vulnerabilities(
    test_token: str, test_config: ForcesConfig
) -> None:
    result = await get_vulnerabilities(test_config, api_token=test_token)
    assert len(result) == 36
    assert "192.168.100.103" in result[0]["where"]


@pytest.mark.asyncio
async def test_vulnerabilities_api_filter_static(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        kind=KindEnum.STATIC,
    )
    result = await get_vulnerabilities(test_config, api_token=test_token)
    for vuln in result:
        assert vuln["vulnerabilityType"] == "lines"


@pytest.mark.asyncio
async def test_vulnerabilities_api_filter_severity(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        breaking_severity=Decimal("3.2"),
        verbose_level=1,
    )
    result = await get_vulnerabilities(test_config, api_token=test_token)
    for vuln in result:
        if vuln["severity"] is not None:
            assert vuln["severity"] >= 3.0


@pytest.mark.asyncio
async def test_vulnerabilities_api_filter_open(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        verbose_level=2,
    )
    result = await get_vulnerabilities(test_config, api_token=test_token)
    for vuln in result:
        assert vuln["state"] in ["VULNERABLE", "ACCEPTED"]  # ZRs & Treatments


@pytest.mark.asyncio
async def test_get_group_access() -> None:
    try:
        await get_groups_access(api_token="bad_token")
    except ApiError as exc:
        assert (
            "Login required" in exc.messages
            or "Token format unrecognized" in exc.messages
        )
