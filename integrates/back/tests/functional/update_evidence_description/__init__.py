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
    description: str,
    draft: str,
    evidence: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
                updateEvidenceDescription(
                description: "{description}",
                findingId: "{draft}",
                evidenceId: {evidence}
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, str] = { 'query': query }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
