from . import (
    get_result,
    get_result_treatments,
)
from custom_exceptions import (
    ReportAlreadyRequested,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_report(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "success" in result["data"]["report"]
    assert result["data"]["report"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["executive@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_get_report_fail(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_report_second_time_fail(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(ReportAlreadyRequested())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email", "treatments"],
    [
        ["admin@gmail.com", ["ACCEPTED", "IN_PROGRESS"]],
        ["user_manager@gmail.com", ["ACCEPTED", "IN_PROGRESS"]],
        ["vulnerability_manager@gmail.com", ["ACCEPTED", "IN_PROGRESS"]],
        ["hacker@gmail.com", ["ACCEPTED", "IN_PROGRESS"]],
        ["customer_manager@fluidattacks.com", ["ACCEPTED", "IN_PROGRESS"]],
    ],
)
async def test_get_report_treatments(
    populate: bool, email: str, treatments: list[str]
) -> None:
    assert populate
    group: str = "group1"
    result_xls: dict[str, Any] = await get_result_treatments(
        user=email,
        group_name=group,
        report_type="XLS",
        treatments=treatments,
    )
    assert "success" in result_xls["data"]["report"]
    assert result_xls["data"]["report"]["success"]

    result_data: dict[str, Any] = await get_result_treatments(
        user=email,
        group_name=group,
        report_type="DATA",
        treatments=treatments,
    )
    assert "success" in result_data["data"]["report"]
    assert result_data["data"]["report"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_report_business_info_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group: str = "group1"
    result_cert: dict[str, Any] = await get_result_treatments(
        user=email,
        group_name=group,
        report_type="CERT",
        treatments=[],
    )
    assert "errors" in result_cert
    assert "Error - " in result_cert["errors"][0]["message"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email", "treatments", "should_fail"],
    [
        ["admin@gmail.com", ["ACCEPTED", "IN_PROGRESS"], True],
        ["admin@gmail.com", ["ACCEPTED"], False],
        ["user_manager@gmail.com", ["ACCEPTED", "IN_PROGRESS"], True],
        ["user_manager@gmail.com", ["ACCEPTED"], False],
        ["vulnerability_manager@gmail.com", ["ACCEPTED", "IN_PROGRESS"], True],
        ["vulnerability_manager@gmail.com", ["ACCEPTED"], False],
        ["hacker@gmail.com", ["ACCEPTED", "IN_PROGRESS"], True],
        ["hacker@gmail.com", ["IN_PROGRESS"], False],
        [
            "customer_manager@fluidattacks.com",
            ["ACCEPTED", "IN_PROGRESS"],
            True,
        ],
        ["customer_manager@fluidattacks.com", ["ACCEPTED"], False],
    ],
)
async def test_get_report_treatments_second_time_fail(
    populate: bool, email: str, treatments: list[str], should_fail: bool
) -> None:
    assert populate
    group: str = "group1"
    result_xls: dict[str, Any] = await get_result_treatments(
        user=email,
        group_name=group,
        report_type="XLS",
        treatments=treatments,
    )
    if should_fail:
        assert "errors" in result_xls
        assert result_xls["errors"][0]["message"] == str(
            ReportAlreadyRequested()
        )
    else:
        assert "success" in result_xls["data"]["report"]
        assert result_xls["data"]["report"]["success"]

    result_data: dict[str, Any] = await get_result_treatments(
        user=email,
        group_name=group,
        report_type="DATA",
        treatments=treatments,
    )
    assert "errors" in result_data
    assert result_data["errors"][0]["message"] == str(ReportAlreadyRequested())
