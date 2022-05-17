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
    organization_name: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.2,
                maxNumberAcceptances: 3,
                minAcceptanceSeverity: 1.5,
                minBreakingSeverity: 5.7,
                vulnerabilityGracePeriod: 1000,
                organizationId: "{organization_id}",
                organizationName: "{organization_name}"
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
