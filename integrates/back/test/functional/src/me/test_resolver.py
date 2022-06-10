# pylint: disable=import-error, useless-suppression, too-many-arguments
from . import (
    get_result,
    get_vulnerabilities,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ("email", "role", "permissions", "phone", "groups_length"),
    (
        (
            "admin@gmail.com",
            "admin",
            18,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "1111111111",
            },
            0,
        ),
        (
            "user@gmail.com",
            "user",
            4,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182132",
            },
            1,
        ),
        (
            "user_manager@gmail.com",
            "user_manager",
            0,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "77777777777777",
            },
            1,
        ),
        (
            "vulnerability_manager@gmail.com",
            "user",
            4,
            {
                "callingCountryCode": "51",
                "countryCode": "PE",
                "nationalNumber": "1111111111111",
            },
            1,
        ),
        (
            "hacker@gmail.com",
            "hacker",
            3,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182131",
            },
            2,
        ),
        (
            "reattacker@gmail.com",
            "reattacker",
            0,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "4444444444444",
            },
            1,
        ),
        (
            "resourcer@gmail.com",
            "resourcer",
            0,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "33333333333",
            },
            1,
        ),
        (
            "reviewer@gmail.com",
            "reviewer",
            0,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "7777777777",
            },
            2,
        ),
        ("service_forces@gmail.com", "service_forces", 0, None, 1),
        (
            "customer_manager@fluidattacks.com",
            "customer_manager",
            0,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "9999999999999",
            },
            1,
        ),
    ),
)
async def test_get_me(
    populate: bool,
    email: str,
    role: str,
    permissions: int,
    phone: int,
    groups_length: int,
) -> None:
    assert populate
    org_name: str = "orgtest"
    organization: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        user=email,
        org_id=organization,
    )
    assert "errors" not in result
    assert '{"hasAccessToken": false' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert not result["data"]["me"]["hasMobileApp"]
    assert not result["data"]["me"]["isConcurrentSession"]
    assert result["data"]["me"]["organizations"][0]["name"] == org_name
    assert (
        len(result["data"]["me"]["organizations"][0]["groups"])
        == groups_length
    )
    assert len(result["data"]["me"]["permissions"]) == permissions
    assert result["data"]["me"]["phone"] == phone
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == role
    assert result["data"]["me"]["subscriptionsToEntityReport"] == []
    assert result["data"]["me"]["tags"] == []
    assert result["data"]["me"]["__typename"] == "Me"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ["email", "length"],
    [
        ["user@gmail.com", 1],
        ["user_manager@gmail.com", 1],
        ["vulnerability_manager@gmail.com", 1],
    ],
)
async def test_get_me_assigned(
    populate: bool, email: str, length: int
) -> None:
    assert populate
    result: dict[str, Any] = await get_vulnerabilities(
        user=email,
    )
    assert "errors" not in result
    assert len(result["data"]["me"]["vulnerabilitiesAssigned"]) == length
