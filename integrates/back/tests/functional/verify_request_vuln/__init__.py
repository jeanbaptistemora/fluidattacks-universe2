# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from back.tests.functional.utils import (
    get_graphql_result,
)


async def query(
    *,
    user: str,
    finding: str,
    vulnerability: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            verifyRequestVuln(
                findingId: "{finding}",
                justification: "Vuln verified",
                openVulns: ["{vulnerability}"],
                closedVulns: []
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = { 'query': query }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
