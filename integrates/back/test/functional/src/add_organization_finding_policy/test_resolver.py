from . import (
    get_result,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_name"),
    (
        ("031. Excessive privileges - AWS"),
        ("009. Sensitive information in source code"),
        ("265. Insecure encryption algorithm - AES"),
    ),
)
async def test_add_organization_finding_policy(
    populate: bool, finding_name: str
) -> None:
    assert populate
    email: str = "user_manager@gmail.com"
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_name=finding_name,
    )
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization_finding_policy")
@pytest.mark.parametrize(
    ("email"),
    (
        ("admin@gmail.com"),
        ("admin@fluidattacks.com"),
    ),
)
async def test_add_organization_finding_policy_fail(
    populate: bool, email: str
) -> None:
    assert populate
    finding_name: str = "063. Lack of data validation - Path Traversal"
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_name=finding_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
