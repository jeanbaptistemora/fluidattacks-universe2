from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_update_finding_description(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email)
    assert "errors" not in result
    assert "success" in result["data"]["updateDescription"]
    assert result["data"]["updateDescription"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email", "unfulfilled_requirements"],
    [
        ["admin@gmail.com", ["266"]],
        ["hacker@gmail.com", ["266"]],
    ],
)
async def test_update_finding_unfulfilled_requirements(
    populate: bool, email: str, unfulfilled_requirements: list[str]
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, unfulfilled_requirements=unfulfilled_requirements
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateDescription"]
    assert result["data"]["updateDescription"]["success"]
    assert (
        len(
            result["data"]["updateDescription"]["finding"][
                "unfulfilledRequirements"
            ]
        )
        == 1
    )
    assert (
        result["data"]["updateDescription"]["finding"][
            "unfulfilledRequirements"
        ][0]["id"]
        == "266"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email", "unfulfilled_requirements"],
    [
        ["admin@gmail.com", ["999"]],
        ["hacker@gmail.com", ["999"]],
    ],
)
async def test_update_finding_invalid_unfulfilled_requirements(
    populate: bool, email: str, unfulfilled_requirements: list[str]
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, unfulfilled_requirements=unfulfilled_requirements
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The requirement is not valid in the vulnerability"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email", "unfulfilled_requirements"],
    [
        ["admin@gmail.com", []],
        ["hacker@gmail.com", []],
    ],
)
async def test_update_finding_empty_unfulfilled_requirements(
    populate: bool, email: str, unfulfilled_requirements: list[str]
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, unfulfilled_requirements=unfulfilled_requirements
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The unfulfilled requirements are required"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email", "description"],
    [
        ["admin@gmail.com", "Duplicated description"],
        ["hacker@gmail.com", "Duplicated description"],
    ],
)
async def test_update_finding_duplicated_description(
    populate: bool, email: str, description: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, description=description
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Finding with the same description already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email", "recommendation"],
    [
        ["admin@gmail.com", "Duplicated recommendation"],
        ["hacker@gmail.com", "Duplicated recommendation"],
    ],
)
async def test_update_finding_duplicated_recommendation(
    populate: bool, email: str, recommendation: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, recommendation=recommendation
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Finding with the same recommendation already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
    ],
)
async def test_update_finding_description_fail(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
