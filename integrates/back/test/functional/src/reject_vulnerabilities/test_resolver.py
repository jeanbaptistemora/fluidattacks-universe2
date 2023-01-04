from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
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
@pytest.mark.resolver_test_group("reject_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id", "justification", "other_justification"),
    (
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "OTHER",
            "other justification test",
        ),
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce11",
            "CONSISTENCY",
            None,
        ),
    ),
)
async def test_reject_vulnerabilities(
    populate: bool,
    email: str,
    vuln_id: str,
    justification: str,
    other_justification: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.SUBMITTED

    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
        justification=justification,
        other_justification=other_justification,
    )
    assert "errors" not in result
    assert result["data"]["rejectVulnerabilities"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vuln = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.REJECTED
    assert vuln.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id", "justification", "other_justification"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
            "CONSISTENCY",
            None,
        ),
    ),
)
async def test_reject_vulnerabilities_fail(
    populate: bool,
    email: str,
    vuln_id: str,
    justification: str,
    other_justification: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
        justification=justification,
        other_justification=other_justification,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
