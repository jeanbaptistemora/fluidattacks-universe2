# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
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
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
