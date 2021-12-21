from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.skip(reason="Temporarily disabled due to db migration")
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("customer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
        ("customeradmin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce12"),
        ("system_owner@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce13"),
    ),
)
async def test_request_vulnerabilities_zero_risk(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert vuln.zero_risk is None

    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["requestVulnerabilitiesZeroRisk"]["success"]

    loaders.vulnerability_typed.clear(vuln_id)
    vuln = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert vuln.zero_risk.status == VulnerabilityZeroRiskStatus.REQUESTED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("executive@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_request_vulnerabilities_zero_risk_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
