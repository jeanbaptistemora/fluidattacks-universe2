# pylint: disable=import-error
from back.test.functional.src.utils import (
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
    attack_vector_description: str = "This is an attack vector"
    description: str = "This is a pytest created draft"
    group: str = "group1"
    recommendation: str = "Solve this finding"
    requirements: str = "REQ.0366. Do something"
    threat: str = "Attacker"
    title: str = "366. Inappropriate coding practices - Transparency Conflict"
    min_time_to_remediate: str = "18"
    query: str = f"""
        mutation {{
            addDraft(
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                groupName: "{group}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                threat: "{threat}",
                title: "{title}",
                minTimeToRemediate: "{min_time_to_remediate}",
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
