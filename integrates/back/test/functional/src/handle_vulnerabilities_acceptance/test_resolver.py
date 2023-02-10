from . import (
    get_result,
)
from custom_exceptions import (
    VulnNotFound,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptance(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()

    accepted_vuln = await loaders.vulnerability.load(accepted_vulnerability_id)
    assert accepted_vuln
    assert accepted_vuln.treatment
    rejected_vuln = await loaders.vulnerability.load(rejected_vulnerability_id)
    assert rejected_vuln
    assert rejected_vuln.treatment
    assert (
        accepted_vuln.treatment.acceptance_status
        == rejected_vuln.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.SUBMITTED
    )
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["handleVulnerabilitiesAcceptance"]["success"]

    loaders.vulnerability.clear_all()
    loaders.vulnerability_historic_treatment.clear(accepted_vulnerability_id)
    accepted_vuln = await loaders.vulnerability.load(accepted_vulnerability_id)
    assert accepted_vuln
    assert accepted_vuln.treatment
    rejected_vuln = await loaders.vulnerability.load(rejected_vulnerability_id)
    assert rejected_vuln
    assert rejected_vuln.treatment
    assert (
        accepted_vuln.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
    )
    assert rejected_vuln.treatment.acceptance_status is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    ("email"),
    (
        ("user_manager@gmail.com"),
        ("vulnerability_manager@gmail.com"),
    ),
)
async def test_handle_vulnerabilities_acceptance_fail_1(
    populate: bool,
    email: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id="6f023c26-5x10-4ded-aa27-xx563c2206ax",
        rejected_vulnerability_id="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(VulnNotFound())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptance_fail_2(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
