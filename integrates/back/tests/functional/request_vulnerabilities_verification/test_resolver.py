from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
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
@pytest.mark.resolver_test_group("request_vulnerabilities_verification")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("customer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
        ("customeradmin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce12"),
        ("executive@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce13"),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce15"),
        ("system_owner@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce16"),
    ),
)
async def test_request_verification_vuln(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["requestVulnerabilitiesVerification"]["success"]

    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    assert finding.verification.status == FindingVerificationStatus.REQUESTED
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        vuln_id
    )
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )
