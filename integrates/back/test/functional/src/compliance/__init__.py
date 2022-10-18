# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    organization_id: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            organization(organizationId: "{organization_id}"){{
                id
                compliance {{
                complianceLevel
                complianceWeeklyTrend
                estimatedDaysToFullCompliance
                standards{{
                    avgOrganizationComplianceLevel
                    bestOrganizationComplianceLevel
                    complianceLevel
                    standardTitle
                    worstOrganizationComplianceLevel
                }}
                }}
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
