from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_access_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["system_owner@gmail.com"],
        ["hacker@gmail.com"],
        ["customer@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_group_info(
    populate: bool,
    email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group_context="Group context test",
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupAccessInfo"]
    assert result["data"]["updateGroupAccessInfo"]["success"]
