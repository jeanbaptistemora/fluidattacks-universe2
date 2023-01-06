# pylint: disable=import-error
from . import (
    get_result,
)
from back.test.functional.src.organization import (
    get_result as get_organization,
)
from custom_exceptions import (
    StakeholderNotInOrganization,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
    ],
)
async def test_update_organization_policies(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    result: dict[str, Any] = await get_result(
        user=email,
        organization_id=org_id,
        organization_name=org_name,
        inactivity_period=270,
        max_acceptance_days=5,
        max_acceptance_severity=8.2,
        max_number_acceptances=3,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.7,
        vulnerability_grace_period=1000,
    )
    assert "errors" not in result
    assert result["data"]["updateOrganizationPolicies"]["success"]

    organization = await get_organization(user=email, org=org_id)
    assert "errors" not in organization
    assert organization["data"]["organization"]["id"] == org_id
    assert organization["data"]["organization"]["inactivityPeriod"] == 270
    assert organization["data"]["organization"]["maxAcceptanceDays"] == 5
    assert organization["data"]["organization"]["maxAcceptanceSeverity"] == 8.2
    assert organization["data"]["organization"]["maxNumberAcceptances"] == 3
    assert organization["data"]["organization"]["minAcceptanceSeverity"] == 0.0
    assert organization["data"]["organization"]["minBreakingSeverity"] == 5.7
    assert (
        organization["data"]["organization"]["vulnerabilityGracePeriod"]
        == 1000
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_organization_policies_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    result: dict[str, Any] = await get_result(
        user=email,
        organization_id=org_id,
        organization_name=org_name,
        inactivity_period=90,
        max_acceptance_days=5,
        max_acceptance_severity=8.2,
        max_number_acceptances=3,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.7,
        vulnerability_grace_period=1000,
    )
    execution = StakeholderNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
    assert result["errors"][0]["message"] == execution.args[0]
