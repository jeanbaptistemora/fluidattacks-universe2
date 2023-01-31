# pylint: disable=import-error
from . import (
    get_group_data,
    get_me_data,
    update_access_token,
)
from back.test.functional.src.add_group import (
    get_result as add_group,
)
import json
import pytest


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
async def test_update_forces_access_token_v1(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await update_access_token(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert not result["data"]["updateForcesAccessToken"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
@pytest.mark.parametrize(
    ["email", "group_name"],
    [
        ["admin@gmail.com", "group21"],
    ],
)
async def test_update_forces_access_token_v2(
    populate: bool,
    email: str,
    group_name: str,
) -> None:
    assert populate

    result_add: dict = await add_group(
        user=email,
        org="orgtest",
        group=group_name,
    )
    assert "errors" not in result_add
    assert result_add["data"]["addGroup"]["success"]

    result: dict = await update_access_token(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["updateForcesAccessToken"]["success"]

    session_jwt: str = result["data"]["updateForcesAccessToken"]["sessionJwt"]
    me_data: dict = await get_me_data(
        user=f"forces.{group_name}@fluidattacks.com"
    )
    assert "errors" not in me_data
    assert (
        json.loads(me_data["data"]["me"]["accessToken"])["lastAccessTokenUse"]
        is None
    )

    group: dict = await get_group_data(
        user=email,
        group=group_name,
        session_jwt=session_jwt,
    )
    assert "errors" not in group
    assert group["data"]["group"]["userRole"] == "service_forces"

    me_data = await get_me_data(user=f"forces.{group_name}@fluidattacks.com")
    assert "errors" not in me_data
    assert (
        json.loads(me_data["data"]["me"]["accessToken"])["lastAccessTokenUse"]
        is None
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_forces_access_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_update_forces_access_token_fail(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await update_access_token(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
