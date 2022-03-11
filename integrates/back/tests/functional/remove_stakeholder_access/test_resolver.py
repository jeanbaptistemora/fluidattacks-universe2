from . import (
    get_access_token,
    get_result,
    put_mutation,
)
from custom_exceptions import (
    ExpiredToken,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_stakeholder_access(populate: bool, email: str) -> None:
    assert populate
    stakeholder_email: str = "admin@gmail.com"
    group_name: str = "group1"
    result: Dict[str, Any] = await put_mutation(
        user=email,
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeStakeholderAccess"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_remove_stakeholder_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    stakeholder_email: str = "hacker@gmail.com"
    group_name: str = "group1"
    result: Dict[str, Any] = await put_mutation(
        user=email,
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.mark.parametrize(
    ["stakeholder_email", "no_access_remaining", "number_organizations"],
    [
        ["justonegroupacess@gmail.com", True, 1],
        ["customer_manager@fluidattacks.com", False, 2],
    ],
)
async def test_remove_stakeholder_remaining_access(
    populate: bool,
    stakeholder_email: str,
    no_access_remaining: bool,
    number_organizations: int,
) -> None:
    assert populate
    email: str = "admin@gmail.com"
    group_name: str = "group4"
    ts_expiration_time: int = int(
        (datetime.utcnow() + timedelta(weeks=8)).timestamp()
    )
    result_jwt = await get_access_token(
        user=stakeholder_email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result_jwt
    assert result_jwt["data"]["updateAccessToken"]["success"]

    session_jwt: str = result_jwt["data"]["updateAccessToken"]["sessionJwt"]
    first_result_query: Dict[str, Any] = await get_result(
        user=stakeholder_email,
        session_jwt=session_jwt,
    )

    assert "errors" not in first_result_query
    assert (
        len(first_result_query["data"]["me"]["organizations"])
        == number_organizations
    )

    result_mutation: Dict[str, Any] = await put_mutation(
        user=email,
        group=group_name,
        stakeholder=stakeholder_email,
    )
    assert "errors" not in result_mutation
    assert "success" in result_mutation["data"]["removeStakeholderAccess"]
    assert result_mutation["data"]["removeStakeholderAccess"]["success"]

    second_result_query: Dict[str, Any] = await get_result(
        user=stakeholder_email,
        session_jwt=session_jwt,
    )
    if no_access_remaining:
        assert "errors" in second_result_query
        assert second_result_query["errors"][0]["message"] == str(
            ExpiredToken()
        )
    else:
        assert "errors" not in second_result_query
        assert (
            len(second_result_query["data"]["me"]["organizations"])
            == number_organizations - 1
        )
