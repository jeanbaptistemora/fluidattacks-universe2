from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files_to_db")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_add_files_to_db(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert result["data"]["addFilesToDb"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files_to_db")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_files_to_db_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
