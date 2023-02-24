from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_update_finding_description(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email)
    assert "errors" not in result
    assert "success" in result["data"]["updateDescription"]
    assert result["data"]["updateDescription"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
    ],
)
async def test_update_finding_description_fail(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
