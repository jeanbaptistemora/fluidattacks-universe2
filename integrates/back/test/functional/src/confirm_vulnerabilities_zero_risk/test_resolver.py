from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingCommentsRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityZeroRiskStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
    ),
)
async def test_confirm_vulnerabilities_zero_risk(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    requested = VulnerabilityZeroRiskStatus.REQUESTED
    assert vulnerability.zero_risk
    assert vulnerability.zero_risk.status == requested

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["confirmVulnerabilitiesZeroRisk"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    confirmed = VulnerabilityZeroRiskStatus.CONFIRMED
    assert vulnerability.zero_risk
    assert vulnerability.zero_risk.status == confirmed
    zero_risk_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.ZERO_RISK, finding_id=finding_id
        )
    )
    assert zero_risk_comments[-1].finding_id == finding_id
    assert zero_risk_comments[-1].content == "confirm zero risk vuln"
    assert zero_risk_comments[-1].comment_type == CommentType.ZERO_RISK
    assert zero_risk_comments[-1].email == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
    ),
)
async def test_confirm_vulnerabilities_zero_risk_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.zero_risk is None

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Zero risk vulnerability is not requested"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user_manager@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_access_denied_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
