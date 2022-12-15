from . import (
    get_result,
)
from custom_exceptions import (
    StakeholderNotInOrganization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
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
        max_acceptance_days=5,
        max_acceptance_severity=8.2,
        max_number_acceptances=3,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.7,
        vulnerability_grace_period=1000,
    )
    assert "errors" not in result
    assert result["data"]["updateOrganizationPolicies"]["success"]

    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(org_id)
    assert organization.policies.max_acceptance_days == 5
    assert organization.policies.max_acceptance_severity == Decimal("8.2")
    assert organization.policies.max_number_acceptances == 3
    assert organization.policies.min_acceptance_severity == Decimal("0.0")
    assert organization.policies.min_breaking_severity == Decimal("5.7")
    assert organization.policies.vulnerability_grace_period == 1000


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
