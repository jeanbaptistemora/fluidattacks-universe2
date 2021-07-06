from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_create_event(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["createEvent"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_create_event_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
