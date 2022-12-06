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
    assert (
        "/integrates/reports/pdf/"
        in result["data"]["unfulfilledStandardReportUrl"]
    )
