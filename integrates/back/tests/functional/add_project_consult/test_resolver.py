from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_project_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customer@gmail.com"],
        ["analyst@gmail.com"],
    ],
)
async def test_add_project_consult(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addProjectConsult"]
    assert result["data"]["addProjectConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_project_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_add_project_consult_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
