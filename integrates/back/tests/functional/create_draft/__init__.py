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
) -> Dict[str, Any]:
    cwe: str = '200'
    description: str = 'This is pytest created draft'
    group: str = 'group1'
    recommendation: str = 'Solve this finding'
    requirements: str = 'REQ.0001. Apply filters'
    risk: str = 'This is pytest created draft'
    threat: str = 'Attacker'
    title: str = 'F001. Very serious vulnerability'
    draft_type: str = 'SECURITY'
    query: str = f"""
        mutation {{
            createDraft(
                cwe: "{cwe}",
                description: "{description}",
                projectName: "{group}",
                recommendation: "{recommendation}",
                requirements: "{requirements}",
                risk: "{risk}",
                threat: "{threat}",
                title: "{title}",
                type: {draft_type}
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
