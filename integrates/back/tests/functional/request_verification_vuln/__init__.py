from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import json
import os
from typing import (
    Any,
    Dict,
)


async def query(
    *,
    user: str,
    finding: str,
    vulnerability: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            requestVerificationVuln(
                findingId: "{finding}",
                justification: "this is a comenting test of a request verification in vulns",
                vulnerabilities:
                    ["{vulnerability}"]
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
