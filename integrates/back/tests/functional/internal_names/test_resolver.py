from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("internal_names")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_admin(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert "internalNames" in result["data"]
    assert result["data"]["internalNames"]["name"] == group


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("internal_names")
@pytest.mark.parametrize(
    ["email"],
    [
        ["closer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_closer(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
