from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_add_files(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert result["data"]["addFiles"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_add_files_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
