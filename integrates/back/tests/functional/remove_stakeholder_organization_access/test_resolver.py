from . import (
    get_organizations,
    get_result,
    put_access_token,
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
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["stakeholder_email", "no_access_remaining", "number_organizations"],
    [
        ["justoneorgacess@test.com", True, 1],
        ["customer_manager@fluidattacks.com", False, 2],
    ],
)
async def test_remove_stakeholder_organization_remaining_access(
    populate: bool,
    stakeholder_email: str,
    no_access_remaining: bool,
    number_organizations: int,
) -> None:
    assert populate
    email: str = "admin@gmail.com"
    org_id: str = "ORG#ed3831e8-14a2-483b-9cff-cc0747829640"
    ts_expiration_time: int = int(
        (datetime.utcnow() + timedelta(weeks=8)).timestamp()
    )
    result_jwt = await put_access_token(
        user=stakeholder_email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result_jwt
    assert result_jwt["data"]["updateAccessToken"]["success"]

    session_jwt: str = result_jwt["data"]["updateAccessToken"]["sessionJwt"]
    first_result_query: Dict[str, Any] = await get_organizations(
        user=stakeholder_email,
        session_jwt=session_jwt,
    )
    assert "errors" not in first_result_query
    assert (
        len(first_result_query["data"]["me"]["organizations"])
        == number_organizations
    )

    result_mutation: Dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        stakeholder=stakeholder_email,
    )
    assert "errors" not in result_mutation
    assert result_mutation["data"]["removeStakeholderOrganizationAccess"][
        "success"
    ]

    second_result_query: Dict[str, Any] = await get_organizations(
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_stakeholder_organization_access(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, stakeholder=email
    )
    assert "errors" not in result
    assert result["data"]["removeStakeholderOrganizationAccess"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_remove_stakeholder_organization_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, stakeholder=email
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
