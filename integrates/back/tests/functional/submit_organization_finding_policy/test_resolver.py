from . import (
    get_result,
)
from custom_exceptions import (
    PolicyAlreadyHandled,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id", "email"),
    (
        (
            "dd63f2df-522d-4bfa-ad85-837832c71164",
            "customer@gmail.com",
        ),
        (
            "3be367f9-b06c-4f72-ab77-38268045a8ff",
            "customeradmin@gmail.com",
        ),
    ),
)
async def test_submit_organization_finding_policy(
    populate: bool, finding_policy_id: str, email: str
) -> None:
    assert populate
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" not in result
    assert result["data"]["submitOrganizationFindingPolicy"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id",),
    (("f3f19b09-00e5-4bc7-b9ea-9999c9fe9f87",),),
)
@pytest.mark.parametrize(
    ("email",),
    (
        ("customer@gmail.com",),
        ("customeradmin@gmail.com",),
    ),
)
async def test_submit_organization_finding_policy_fail_1(
    populate: bool, finding_policy_id: str, email: str
) -> None:
    assert populate
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(PolicyAlreadyHandled())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id",),
    (
        ("dd63f2df-522d-4bfa-ad85-837832c71164",),
        ("3be367f9-b06c-4f72-ab77-38268045a8ff",),
    ),
)
@pytest.mark.parametrize(
    ("email",),
    (
        ("hacker@gmail.com",),
        ("closer@gmail.com",),
    ),
)
async def test_submit_organization_finding_policy_fail_2(
    populate: bool, finding_policy_id: str, email: str
) -> None:
    assert populate
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
