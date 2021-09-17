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


async def get_result(  # pylint: disable=too-many-locals
    *,
    user: str,
) -> Dict[str, Any]:
    finding_id: str = "475041513"
    affected_systems: str = "Server bWAPP"
    attack_vector_description: str = "This is an updated attack vector"
    records: str = "Clave plana"
    records_number: int = 12
    description: str = "I just have updated the description"
    recommendation: str = "Updated recommendation"
    threat: str = "Updated threat"
    finding_type: str = "SECURITY"
    query: str = f"""
        mutation {{
            updateDescription(
                affectedSystems: "{affected_systems}",
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                recordsNumber: {records_number},
                threat: "{threat}",
                findingType: "{finding_type}"
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
