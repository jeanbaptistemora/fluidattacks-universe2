# pylint: disable=too-many-arguments
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
        [
            "admin@gmail.com",
            "This is an attack vector 2",
            "Solve this finding 2",
        ],
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
            "min_time_to_remediate",
            "Solve this finding",
            0,
        ],
        [
            "admin@gmail.com",
            "min_time_to_remediate",
            "Solve this finding",
            -1,
        ],
    ],
)
async def test_add_finding_positive_min_time_to_remediate(
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "recommendation", "unfulfilled_requirements"],
    [
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Solve this finding",
            ["-21"],
        ],
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Solve this finding",
            [""],
        ],
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Solve this finding",
            ["158", "21212121"],
        ],
    ],
)
async def test_add_finding_requirements_in_criteria(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    unfulfilled_requirements: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The requirement is not valid in the vulnerability"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "recommendation", "title"],
    [
        [
            "admin@gmail.com",
            "invalid_title",
            "Solve this finding",
            "F001. Test",
        ],
        [
            "admin@gmail.com",
            "invalid_title",
            "Solve this finding",
            "Test",
        ],
        [
            "admin@gmail.com",
            "invalid_title",
            "Solve this finding",
            "001",
        ],
    ],
)
async def test_add_finding_invalid_title(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    title: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        title=title,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The inserted Draft/Finding title is invalid"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "recommendation",
        "title",
        "unfulfilled_requirements",
    ],
    [
        [
            "admin@gmail.com",
            "duplicated_recommendation",
            "Updated recommendation",
            "001. SQL injection - C Sharp SQL API",
            ["169"],
        ],
    ],
)
async def test_add_finding_duplicated_recommendation(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    title: str,
    unfulfilled_requirements: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        title=title,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Finding with the same recommendation already exists"
    )
