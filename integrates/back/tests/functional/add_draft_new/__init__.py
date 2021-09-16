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
) -> Dict[str, Any]:
    affected_systems: str = "Server bWAPP"
    attack_vector_description: str = "This is an attack vector"
    description: str = "This is pytest created draft"
    group: str = "group1"
    recommendation: str = "Solve this finding"
    requirements: str = "REQ.0001. Apply filters"
    threat: str = "Attacker"
    title: str = "001. SQL injection - C Sharp SQL API"
    query: str = f"""
        mutation {{
            addDraft(
                affectedSystems: "{affected_systems}",
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                groupName: "{group}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                threat: "{threat}",
                title: "{title}",
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
