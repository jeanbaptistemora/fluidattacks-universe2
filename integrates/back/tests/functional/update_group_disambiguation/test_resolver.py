from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_disambiguation")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["resourcer@gmail.com"],
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
        disambiguation="disambiguation test",
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupDisambiguation"]
    assert result["data"]["updateGroupDisambiguation"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_disambiguation")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customeradmin@gmail.com"],
        ["customer@gmail.com"],
        ["reattacker@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_group_info_fail(
    populate: bool,
    email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        disambiguation="Disambiguation test",
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
