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
    org: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            organization(organizationId: "{org}") {{
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptations
                minAcceptanceSeverity
                name
                groups {{
                    name
                }}
                stakeholders {{
                    email
                }}
                permissions(identifier: "{group}")
                userRole(identifier: "{group}")
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
