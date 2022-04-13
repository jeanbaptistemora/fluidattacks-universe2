from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicators,
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
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email", "finding_id", "vuln_id"],
    [
        [
            "admin@gmail.com",
            "3c475384-834c-47b0-ac71-a41a022e401c",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
        ],
        [
            "reviewer@gmail.com",
            "475041520",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ],
    ],
)
async def test_approve_draft(
    populate: bool, email: str, finding_id: str, vuln_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["approveDraft"]
    assert result["data"]["approveDraft"]["success"]

    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    assert finding.state.status == FindingStateStatus.APPROVED

    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    approval_date: str = finding.approval.modified_date
    assert vuln.unreliable_indicators.unreliable_report_date == approval_date
    finding_indicators: FindingUnreliableIndicators = (
        finding.unreliable_indicators
    )
    assert (
        finding_indicators.unreliable_newest_vulnerability_report_date
        == approval_date
    )
    assert (
        finding_indicators.unreliable_oldest_open_vulnerability_report_date
        == ""
    )
    assert (
        finding_indicators.unreliable_oldest_vulnerability_report_date
        == approval_date
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["hacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["reattacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["executive@gmail.com", "475041520"],
    ],
)
async def test_approve_draft_fail(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
