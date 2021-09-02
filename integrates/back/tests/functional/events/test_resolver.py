from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_get_events(populate: bool, email: str) -> None:
    assert populate
    expected: List[Dict[str, str]] = [
        {
            "id": "418900971",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "evidence": "evidence1",
            "detail": "ASM unit test1",
        },
        {
            "id": "418900980",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "evidence": "evidence2",
            "detail": "ASM unit test2",
        },
    ]
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert result["data"]["events"] == expected
