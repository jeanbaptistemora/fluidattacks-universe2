from . import (
    get_result,
)
from custom_exceptions import (
    AlreadyOnHold,
    NotVerificationRequested,
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
from db_model.findings.enums import (
    FindingVerificationStatus as FVStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_hold")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("hacker@fluidattacks.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        (
            "reattacker@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce11",
        ),
        (
            "architect@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce12",
        ),
        (
            "resourcer@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce13",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce14",
        ),
    ),
)
async def test_request_hold_vuln(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    event_id: str = "418900971"
    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert (
        vulnerability.unreliable_indicators.unreliable_last_reattack_requester
        != ""
    )
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )
    assert finding.verification
    assert finding.verification.modified_by != email

    result: dict[str, Any] = await get_result(
        user=email, event=event_id, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["requestVulnerabilitiesHold"]["success"]

    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.verification
    assert finding.verification.status == FVStatus.ON_HOLD
    assert finding.verification.modified_by == email
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.ON_HOLD
    )
    assert (
        vulnerability.unreliable_indicators.unreliable_last_reattack_requester
        != email
    )
    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_comments[-1].finding_id == finding_id
    assert finding_comments[-1].comment_type == CommentType.VERIFICATION
    assert finding_comments[-1].email == email
    assert finding_comments[-1].content == (
        f"These reattacks have been put on hold because of Event #{event_id}"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_hold")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("hacker@fluidattacks.com", "be09edb7-cd5c-47ed-bee4-97c645acdce15"),
        ("hacker@fluidattacks.com", "be09edb7-cd5c-47ed-bee4-97c645acdce16"),
    ),
)
async def test_request_hold_vuln_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(
        user=email, event=event_id, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(AlreadyOnHold()) or result[
        "errors"
    ][0]["message"] == str(NotVerificationRequested())
