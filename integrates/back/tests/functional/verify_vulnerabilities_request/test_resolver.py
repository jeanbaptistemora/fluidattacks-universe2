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
    ("email", "vuln_id", "new_status"),
    (
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            VulnerabilityStateStatus.OPEN,
        ),
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.OPEN,
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdcea",
            VulnerabilityStateStatus.CLOSED,
        ),
    ),
)
async def test_request_vulnerabilities_verification(
    populate: bool,
    email: str,
    vuln_id: str,
    new_status: VulnerabilityStateStatus,
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
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )
    assert "errors" not in result
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]

    finding: Finding = await loaders.finding.load(finding_id)
    assert finding.verification.status == FindingVerificationStatus.VERIFIED
    assert vuln_id in finding.verification.vulnerability_ids
    assert finding.verification.modified_by == email
    loaders.vulnerability_typed.clear(vuln_id)
    vuln = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.state.status == new_status
    assert vuln.verification.status == VulnerabilityVerificationStatus.VERIFIED
