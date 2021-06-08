from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
async def test_admin(populate: bool) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user="admin@gmail.com",
        group="group1",
    )
    assert "errors" not in result
    assert not result["data"]["updateForcesAccessToken"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
async def test_analyst(populate: bool) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user="analyst@gmail.com",
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
async def test_closer(populate: bool) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user="closer@gmail.com",
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
