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
    email: str,
    organization_id: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            organization(organizationId: "{organization_id}"){{
                id
                findingPolicies {{
                    id
                    name
                    status
                    lastStatusUpdate
                }}
            }}
        }}
    """
    data = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
