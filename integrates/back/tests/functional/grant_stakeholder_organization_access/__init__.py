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
    role: str,
    email: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            grantStakeholderOrganizationAccess(
                organizationId: "{org}"
                role: {role}
                userEmail: "{email}"
            ) {{
                success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
