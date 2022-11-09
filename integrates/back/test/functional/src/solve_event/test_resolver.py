# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
    FindingCommentsRequest,
)
from db_model.findings.enums import (
    FindingVerificationStatus as FinVStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import pytest
from typing import (
    Any,
)
from vulnerabilities.domain.core import (
    get_reattack_requester,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email", "event_id"],
    [
        ["admin@gmail.com", "418900971"],
        ["hacker@gmail.com", "418900972"],
        ["reattacker@gmail.com", "418900973"],
        ["resourcer@gmail.com", "418900974"],
    ],
)
async def test_solve_event(populate: bool, email: str, event_id: str) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.CREATED

    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["solveEvent"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.SOLVED
    assert event.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_solve_event_fail(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email", "event_id"],
    [
        ["customer_manager@fluidattacks.com", "418900975"],
    ],
)
async def test_solve_event_on_hold(
    populate: bool, email: str, event_id: str
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    finding: Finding = await loaders.finding.load(
        "3c475384-834c-47b0-ac71-a41a022e401c"
    )
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd"
    )
    assert event.state.status == EventStateStatus.CREATED
    assert finding.verification.status == FinVStatus.ON_HOLD  # type: ignore
    assert finding.verification.modified_by == email  # type: ignore
    assert (
        vulnerability.verification.status  # type: ignore
        == VulnerabilityVerificationStatus.ON_HOLD
    )

    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["solveEvent"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    finding = await loaders.finding.load(
        "3c475384-834c-47b0-ac71-a41a022e401c"
    )
    vulnerability = await loaders.vulnerability.load(
        "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd"
    )
    requester = await get_reattack_requester(loaders, vulnerability)
    solve_consult: str = "The reattacks are back to"
    consults: tuple[FindingComment, ...] = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding.id
        )
    )
    assert event.state.status == EventStateStatus.SOLVED
    assert event.state.modified_by == email
    assert any(solve_consult in consult.content for consult in consults)
    assert finding.verification.status == FinVStatus.REQUESTED  # type: ignore
    assert finding.verification.modified_by != email  # type: ignore
    assert finding.verification.modified_by == requester  # type: ignore
    assert (
        vulnerability.unreliable_indicators.unreliable_last_reattack_requester
        == requester
    )
    assert (
        vulnerability.verification.status  # type: ignore
        == VulnerabilityVerificationStatus.REQUESTED
    )
    assert any(email in consult.email for consult in consults)
    assert not any(requester in consult.email for consult in consults)
