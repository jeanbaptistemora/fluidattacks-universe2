from . import (
    update_group_policies,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
    ],
)
async def test_update_group_policies(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await update_group_policies(
        group_name=group_name,
        max_acceptance_days=30,
        max_acceptance_severity=6.9,
        max_number_acceptances=2,
        min_acceptance_severity=0.0,
        min_breaking_severity=7.0,
        user=email,
        vulnerability_grace_period=61,
    )
    assert "errors" not in result
    assert result["data"]["updateGroupPolicies"]["success"]

    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.policies
    assert group.policies.max_acceptance_days == 30
    assert group.policies.max_acceptance_severity == Decimal("6.9")
    assert group.policies.max_number_acceptances == 2
    assert group.policies.min_acceptance_severity == Decimal("0.0")
    assert group.policies.min_breaking_severity == Decimal("7.0")
    assert group.policies.vulnerability_grace_period == 61


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_policies")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_update_group_policies_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await update_group_policies(
        group_name=group_name,
        max_acceptance_days=5,
        max_acceptance_severity=8.2,
        max_number_acceptances=3,
        min_acceptance_severity=1.0,
        min_breaking_severity=5.0,
        user=email,
        vulnerability_grace_period=10,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
