from . import (
    get_result,
)
from custom_exceptions import (
    InvalidFieldLength,
    OnlyCorporateEmails,
    TrialRestriction,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
async def test_admin(populate: bool) -> None:
    assert populate
    org_name: str = "TESTORG"
    result: Dict[str, Any] = await get_result(
        user="admin@fluidattacks.com", org=org_name
    )
    assert "errors" not in result
    assert result["data"]["addOrganization"]["success"]
    assert (
        result["data"]["addOrganization"]["organization"]["name"]
        == org_name.lower()
    )
    assert result["data"]["addOrganization"]["organization"]["id"].startswith(
        "ORG#"
    )
    assert not result["data"]["addOrganization"]["organization"][
        "id"
    ].startswith("ORG#ORG#")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
async def test_analyst(populate: bool) -> None:
    assert populate
    org_name: str = "TESTORG"
    result: Dict[str, Any] = await get_result(
        user="hacker@fluidattacks.com", org=org_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Name taken"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
@pytest.mark.parametrize(
    ["email", "org_name"],
    [
        ["admin@fluidattacks.com", "a" * 1],
        ["admin@fluidattacks.com", "a" * 2],
        ["admin@fluidattacks.com", "a" * 3],
        ["admin@fluidattacks.com", "a" * 11],
    ],
)
async def test_add_organization_invalid_name_fail(
    populate: bool, email: str, org_name: str
) -> None:
    assert populate
    result: dict = await get_result(user=email, org=org_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidFieldLength())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
async def test_personal(populate: bool) -> None:
    assert populate
    org_name: str = "TESTORG"
    result: Dict[str, Any] = await get_result(
        user="hacker@gmail.com", org=org_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == OnlyCorporateEmails().args[0]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
@pytest.mark.parametrize(
    ["email"],
    [
        ["johndoe@johndoe.com"],
        ["janedoe@janedoe.com"],
    ],
)
async def test_only_one_org_during_trial(populate: bool, email: str) -> None:
    assert populate
    result = await get_result(user=email, org="anotherorg")
    assert "errors" in result
    assert result["errors"][0]["message"] == TrialRestriction().args[0]
