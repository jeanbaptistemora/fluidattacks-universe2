from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
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
async def test_get_events(populate: bool, email: str) -> None:
    assert populate
    expected: list[dict[str, str]] = [
        {
            "id": "418900971",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ARM unit test1",
        },
        {
            "id": "418900980",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ARM unit test2",
        },
    ]
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert "events" in result["data"]
    assert result["data"]["events"] == expected
