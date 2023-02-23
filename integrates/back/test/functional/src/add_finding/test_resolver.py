from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "recommendation"],
    [
        ["admin@gmail.com", "This is an attack vector", "Solve this finding"],
    ],
)
async def test_add_finding(
    populate: bool, email: str, description: str, recommendation: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, description=description, recommendation=recommendation
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFinding"]
    assert result["data"]["addFinding"]["success"]
    loaders = get_new_context()
    group_findings = await loaders.group_drafts_and_findings.load("group1")
    new_finding = next(
        finding
        for finding in group_findings
        if finding.description == description
        and finding.recommendation == recommendation
    )
    assert new_finding.state.status is FindingStateStatus.CREATED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "recommendation"],
    [
        ["user@gmail.com", "This is an attack vector", "Solve this finding"],
    ],
)
async def test_add_finding_access_denied(
    populate: bool, email: str, description: str, recommendation: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, description=description, recommendation=recommendation
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "recommendation", "min_time_to_remediate"],
    [
        [
            "admin@gmail.com",
            "This is an attack vector",
            "Solve this finding",
            0,
        ],
        [
            "admin@gmail.com",
            "This is an attack vector",
            "Solve this finding",
            -1,
        ],
    ],
)
async def test_add_finding_min_time_to_remediate_fail(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    min_time_to_remediate: int,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        min_time_to_remediate=min_time_to_remediate,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Min time to remediate should be a positive number"
    )
