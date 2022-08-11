from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
    ),
)
async def test_reject_vulnerabilities_zero_risk(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert vuln.zero_risk.status == VulnerabilityZeroRiskStatus.REQUESTED

    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["rejectVulnerabilitiesZeroRisk"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vuln = await loaders.vulnerability.load(vuln_id)
    assert vuln.state.status == VulnerabilityStateStatus.OPEN
    assert vuln.zero_risk.status == VulnerabilityZeroRiskStatus.REJECTED
    zero_risk_comments: list[
        FindingComment
    ] = await loaders.finding_comments.load(
        (CommentType.ZERO_RISK, finding_id)
    )
    assert zero_risk_comments[-1].finding_id == finding_id
    assert zero_risk_comments[-1].content == "reject zero risk vuln"
    assert zero_risk_comments[-1].comment_type == "zero_risk"
    assert zero_risk_comments[-1].email == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
    ),
)
async def test_reject_vulnerabilities_zero_risk_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vuln.zero_risk is None

    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Zero risk vulnerability is not requested"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
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
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
