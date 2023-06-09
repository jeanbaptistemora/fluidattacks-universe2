from . import (
    approve_draft,
)
from custom_exceptions import (
    IncompleteDraft,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    FindingUnreliableIndicators,
)
import pytest


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
    result: dict = await approve_draft(user=email, finding_id=finding_id)
    assert "errors" not in result
    assert "success" in result["data"]["approveDraft"]
    assert result["data"]["approveDraft"]["success"]

    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.state.status == FindingStateStatus.APPROVED
    assert finding.approval
    approval_date: datetime = finding.approval.modified_date
    finding_indicators: FindingUnreliableIndicators = (
        finding.unreliable_indicators
    )
    assert (
        finding_indicators.unreliable_newest_vulnerability_report_date
        == approval_date
    )
    assert (
        finding_indicators.unreliable_oldest_open_vulnerability_report_date
        is None
    )
    assert (
        finding_indicators.unreliable_oldest_vulnerability_report_date
        == approval_date
    )
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.created_date == approval_date


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_approve_draft_fail_1(populate: bool, email: str) -> None:
    assert populate
    result: dict = await approve_draft(
        user=email, finding_id="8bf3c5e8-1e90-452c-b89d-f9be9eff197b"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(
        IncompleteDraft(["evidences"])
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["hacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["reattacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_approve_draft_fail_2(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: dict = await approve_draft(user=email, finding_id=finding_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
