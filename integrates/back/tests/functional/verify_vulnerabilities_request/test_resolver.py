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
    VulnerabilityStateStatus,
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdcea"),
    ),
)
async def test_request_vulnerabilities_verification(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert (
        vuln.verification.status == VulnerabilityVerificationStatus.REQUESTED
    )

    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]

    finding: Finding = await loaders.finding.load(finding_id)
    assert finding.verification.status == FindingVerificationStatus.VERIFIED
    assert vuln_id in finding.verification.vulnerability_ids
    assert finding.verification.modified_by == email
    loaders.vulnerability_typed.clear(vuln_id)
    vuln: Vulnerability = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert vuln.verification.status == VulnerabilityVerificationStatus.VERIFIED
