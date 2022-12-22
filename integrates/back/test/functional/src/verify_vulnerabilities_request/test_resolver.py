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
    VulnerabilityVerificationStatus as VVerifStatus,
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
            VulnerabilityStateStatus.VULNERABLE,
        ),
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.VULNERABLE,
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdcea",
            VulnerabilityStateStatus.SAFE,
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
    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vuln.verification.status == VVerifStatus.REQUESTED  # type: ignore

    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )
    assert "errors" not in result
    assert "success" in result["data"]["verifyVulnerabilitiesRequest"]
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]

    finding: Finding = await loaders.finding.load(finding_id)
    assert (
        finding.verification.status  # type: ignore
        == FindingVerificationStatus.VERIFIED
    )
    assert vuln_id in finding.verification.vulnerability_ids  # type: ignore
    assert finding.verification.modified_by == email  # type: ignore
    loaders.vulnerability.clear(vuln_id)
    vuln = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == new_status
    assert vuln.verification.status == VVerifStatus.VERIFIED  # type: ignore


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id", "new_status"),
    (
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.VULNERABLE,
        ),
    ),
)
async def test_request_vulnerabilities_verification_fail_1(
    populate: bool,
    email: str,
    vuln_id: str,
    new_status: VulnerabilityStateStatus,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Error verification not requested"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id", "new_status"),
    (
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            VulnerabilityStateStatus.VULNERABLE,
        ),
        (
            "vulnerability_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.SAFE,
        ),
    ),
)
async def test_request_vulnerabilities_verification_fail_2(
    populate: bool,
    email: str,
    vuln_id: str,
    new_status: VulnerabilityStateStatus,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
