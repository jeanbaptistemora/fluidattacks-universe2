from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
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

    accepted_vuln: Vulnerability = await loaders.vulnerability.load(
        accepted_vulnerability_id
    )
    rejected_vuln: Vulnerability = await loaders.vulnerability.load(
        rejected_vulnerability_id
    )
    assert (
        accepted_vuln.treatment.acceptance_status  # type: ignore
        == rejected_vuln.treatment.acceptance_status  # type: ignore
        == VulnerabilityAcceptanceStatus.SUBMITTED
    )
    result: Dict[str, Any] = await get_result(
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
    rejected_vuln = await loaders.vulnerability.load(rejected_vulnerability_id)
    assert (
        accepted_vuln.treatment.acceptance_status  # type: ignore
        == VulnerabilityAcceptanceStatus.APPROVED
    )
    assert rejected_vuln.treatment.acceptance_status is None  # type: ignore


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
async def test_handle_vulnerabilities_acceptance_fail(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
