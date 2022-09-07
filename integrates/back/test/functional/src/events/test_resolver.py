# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    expected: List[Dict[str, str]] = [
        {
            "id": "418900971",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ASM unit test1",
        },
        {
            "id": "418900980",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ASM unit test2",
        },
    ]
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert result["data"]["events"] == expected
