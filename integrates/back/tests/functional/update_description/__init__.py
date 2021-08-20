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
    actor: str = "ANYONE_INTERNET"
    affected_systems: str = "Server bWAPP"
    attack_vector_description: str = "This is an updated attack vector"
    records: str = "Clave plana"
    records_number: int = 12
    description: str = "I just have updated the description"
    recommendation: str = "Updated recommendation"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    scenario: str = "UNAUTHORIZED_USER_EXTRANET"
    threat: str = "Updated threat"
    title: str = "051. Weak passwords reversed"
    finding_type: str = "SECURITY"
    query: str = f"""
        mutation {{
            updateDescription(
                actor: "{actor}",
                affectedSystems: "{affected_systems}",
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                recordsNumber: {records_number},
                requirements: "{requirements}",
                scenario: "{scenario}",
                threat: "{threat}",
                title: "{title}",
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
