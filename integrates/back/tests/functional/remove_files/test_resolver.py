# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_files(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert result["data"]["removeFiles"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
    ],
)
async def test_remove_files_fail_1(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert not result["data"]["removeFiles"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_remove_files_fail_2(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
