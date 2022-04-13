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
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_forces_access_token(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert not result["data"]["updateForcesAccessToken"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_update_forces_access_token_fail(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
