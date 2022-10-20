# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_group,
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
@pytest.mark.resolver_test_group("compliance")
async def test_get_compliance(populate: bool, email: str) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        user=email, organization_id=org_id
    )
    standard_1 = {
        "avgOrganizationComplianceLevel": 0.5,
        "bestOrganizationComplianceLevel": 0.5,
        "complianceLevel": 0.0,
        "standardTitle": "BSIMM",
        "worstOrganizationComplianceLevel": 0.5,
    }
    assert (
        standard_1 in result["data"]["organization"]["compliance"]["standards"]
    )
    group_1: dict[str, Any] = await get_group(user=email, group="group1")
    assert group_1 == {
        "data": {
            "group": {
                "name": "group1",
                "compliance": {
                    "unfulfilledStandards": [
                        {
                            "title": "BSIMM",
                            "unfulfilledRequirements": [
                                {"id": "155"},
                                {"id": "159"},
                                {"id": "273"},
                            ],
                        }
                    ]
                },
            }
        }
    }
