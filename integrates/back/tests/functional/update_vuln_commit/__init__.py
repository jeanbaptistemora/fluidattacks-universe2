# Standard libraries
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
    stakeholder: str,
    vuln_id: str,
) -> Dict[str, Any]:
    return await get_graphql_result(
        {
            "query": f"""
                mutation {{
                    updateVulnCommit(
                        vulnId: "{vuln_id}"
                    ){{
                        success
                    }}
                }}
            """,
        },
        stakeholder=stakeholder,
        context=get_new_context(),
    )
