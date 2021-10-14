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
    finding: str,
    vulnerability: str,
) -> Dict[str, Any]:
    justification: str = "this is a comenting test of a request "
    "verification in vulns"  # pylint: disable=pointless-string-statement
    query: str = f"""
        mutation {{
            requestVulnerabilitiesVerification(
                findingId: "{finding}",
                justification: "{justification}",
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
