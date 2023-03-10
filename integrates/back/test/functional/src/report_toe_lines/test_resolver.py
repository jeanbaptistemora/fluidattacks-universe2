# pylint: disable=import-error
from . import (
    put_mutation,
)
from back.test.functional.src.report import (
    run,
)
from custom_exceptions import (
    ReportAlreadyRequested,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_report_toe_lines(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: dict = await put_mutation(
        user=email,
        group_name=group,
        verification_code="123123",
    )
    assert result["data"]["toeLinesReport"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_report_toe_lines_second_time_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group: str = "group1"
    result: dict = await put_mutation(
        user=email,
        group_name=group,
        verification_code="456456",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(ReportAlreadyRequested())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_toe_lines")
@pytest.mark.parametrize(
    ["email", "group"],
    [
        ["admin@gmail.com", "group1"],
        ["user@gmail.com", "group1"],
    ],
)
async def test_get_report_toe_lines_second_time(
    populate: bool,
    email: str,
    group: str,
) -> None:
    assert populate
    assert (
        await run(
            entity=group,
            additional_info="TOE_LINES",
            subject=email,
        )
        == 0
    )
    result: dict = await put_mutation(
        user=email,
        group_name=group,
        verification_code="789789",
    )
    assert result["data"]["toeLinesReport"]["success"]
