from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
import pytest
from typing import (
    Any,
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

    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )
    assert "errors" not in result
    assert "success" in result["data"]["verifyVulnerabilitiesRequest"]
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.verification
    assert finding.verification.status == FindingVerificationStatus.VERIFIED
    assert finding.verification.vulnerability_ids
    assert vuln_id in finding.verification.vulnerability_ids
    assert finding.verification.modified_by == email
    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == new_status
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
    )


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

    result: dict[str, Any] = await get_result(
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

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability_id=vuln_id,
        status_after_verification=new_status,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
