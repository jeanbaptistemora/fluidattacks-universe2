from . import (
    get_result,
)
from custom_exceptions import (
    StakeholderNotInOrganization,
)
from dataloaders import (
    get_new_context,
)
from organizations.domain import (
    complete_register_for_organization_invitation,
    get_stakeholders,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_grant_stakeholder_organization_access(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6dc"
    stakeholder_email: str = "test2@gmail.com"
    stakeholder_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        role=stakeholder_role,
        email=stakeholder_email,
    )
    assert "errors" not in result
    assert result["data"]["grantStakeholderOrganizationAccess"]["success"]
    assert (
        result["data"]["grantStakeholderOrganizationAccess"][
            "grantedStakeholder"
        ]["email"]
        == stakeholder_email
    )

    loaders = get_new_context()
    stakeholders_access = await loaders.organization_stakeholders_access.load(
        org_id
    )
    # Check stakeholders are created empty when the invitation is pending
    stakeholder_access = stakeholders_access[0]
    assert stakeholder_access.invitation
    assert not stakeholder_access.invitation.is_used
    stakeholders = await get_stakeholders(loaders, org_id)
    assert not stakeholders[0].is_registered

    # When invitation is accepted the stakeholder is updated
    await complete_register_for_organization_invitation(
        loaders, stakeholder_access
    )
    updated_loader = get_new_context()
    stakeholders_access_updated = await (
        updated_loader.organization_stakeholders_access.load(org_id)
    )
    stakeholder_access_updated = stakeholders_access_updated[0]
    stakeholders_updated = await get_stakeholders(updated_loader, org_id)
    assert stakeholder_access_updated.invitation
    assert stakeholder_access_updated.invitation.is_used
    assert stakeholders_updated[0].is_registered


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_organization_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_grant_stakeholder_organization_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6dc"
    stakeholder_email: str = "test2@gmail.com"
    stakeholder_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        role=stakeholder_role,
        email=stakeholder_email,
    )
    execution = StakeholderNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
    assert result["errors"][0]["message"] == execution.args[0]
