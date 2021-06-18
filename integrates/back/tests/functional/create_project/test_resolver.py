from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_project")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_create_project(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["createProject"]
    assert result["data"]["createProject"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_project")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_create_project_fail(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
