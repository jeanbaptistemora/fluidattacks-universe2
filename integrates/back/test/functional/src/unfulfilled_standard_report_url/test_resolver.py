from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
@pytest.mark.resolver_test_group("unfulfilled_standard_report_url")
async def test_get_unfulfilled_standard_report_url(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email, group_name=group_name
    )
    assert "/reports/pdf/" in result["data"]["unfulfilledStandardReportUrl"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "unfulfilled_standards"],
    [
        ["admin@gmail.com", ["bsimm"]],
        ["hacker@gmail.com", ["bsimm"]],
        ["reattacker@gmail.com", ["bsimm"]],
        ["user@gmail.com", ["bsimm"]],
        ["user_manager@gmail.com", ["bsimm"]],
        ["vulnerability_manager@gmail.com", ["bsimm"]],
        ["resourcer@gmail.com", ["bsimm"]],
        ["reviewer@gmail.com", ["bsimm"]],
        ["customer_manager@fluidattacks.com", ["bsimm"]],
    ],
)
@pytest.mark.resolver_test_group("unfulfilled_standard_report_url")
async def test_get_filtered_unfulfilled_standard_report_url(
    populate: bool, email: str, unfulfilled_standards: list[str] | None
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group_name,
        unfulfilled_standards=unfulfilled_standards,
    )
    assert "/reports/pdf/" in result["data"]["unfulfilledStandardReportUrl"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "unfulfilled_standards"],
    [
        ["admin@gmail.com", []],
    ],
)
@pytest.mark.resolver_test_group("unfulfilled_standard_report_url")
async def test_invalid_unfulfilled_standards(
    populate: bool, email: str, unfulfilled_standards: list[str] | None
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group_name,
        unfulfilled_standards=unfulfilled_standards,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Field unfulfilledStandards is invalid"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "unfulfilled_standards"],
    [
        ["admin@gmail.com", ["test_standard_error"]],
    ],
)
@pytest.mark.resolver_test_group("unfulfilled_standard_report_url")
async def test_invalid_standard_id(
    populate: bool, email: str, unfulfilled_standards: list[str] | None
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group_name,
        unfulfilled_standards=unfulfilled_standards,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The standard id is invalid"
    )
