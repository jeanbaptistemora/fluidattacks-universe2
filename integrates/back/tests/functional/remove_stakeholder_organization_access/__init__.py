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


async def query(
    *,
    user: str,
    org: str,
    stakeholder: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org}",
                userEmail: "{stakeholder}"
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
