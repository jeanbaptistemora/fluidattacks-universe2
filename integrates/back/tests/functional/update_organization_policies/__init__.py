from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    identifier: str,
    name: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.5,
                maxNumberAcceptances: 3,
                minAcceptanceSeverity: 1.5,
                organizationId: "{identifier}",
                organizationName: "{name}"
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
