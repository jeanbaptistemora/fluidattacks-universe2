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
    org_id: str,
) -> Dict[str, Any]:
    frecuency: str = "MONTHLY"
    entity: str = "ORGANIZATION"
    query: str = f"""
        mutation {{
            subscribeToEntityReport(
                frequency: {frecuency},
                reportEntity: {entity},
                reportSubject: "{org_id}"


            ) {{
                success
            }}
        }}
    """
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
