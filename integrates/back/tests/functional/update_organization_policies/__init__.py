# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def query(
    *,
    user: str,
    id: str,
    name: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.5,
                maxNumberAcceptations: 3,
                minAcceptanceSeverity: 1.5,
                organizationId: "{id}",
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
