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
) -> Dict[str, Any]:
    affected_systems: str = "Server bWAPP"
    attack_vector_desc: str = "This is an attack vector"
    cwe: str = "200"
    description: str = "This is pytest created draft"
    group: str = "group1"
    recommendation: str = "Solve this finding"
    requirements: str = "REQ.0001. Apply filters"
    risk: str = "This is pytest created draft"
    threat: str = "Attacker"
    title: str = "F001. Very serious vulnerability"
    draft_type: str = "SECURITY"
    query: str = f"""
        mutation {{
            createDraft(
                affectedSystems: "{affected_systems}",
                attackVectorDesc: "{attack_vector_desc}",
                cwe: "{cwe}",
                description: "{description}",
                projectName: "{group}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                risk: "{risk}",
                threat: "{threat}",
                title: "{title}",
                type: {draft_type},
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
