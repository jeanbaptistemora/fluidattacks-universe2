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
                groups {{
                    name
                    compliance {{
                        unfulfilledStandards {{
                            title
                            unfulfilledRequirements {{
                                id
                            }}
                        }}
                    }}
                }}
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


async def get_group(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            group(groupName: "{group}"){{
                name
                compliance {{
                    unfulfilledStandards {{
                        title
                        unfulfilledRequirements {{
                            id
                        }}
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
