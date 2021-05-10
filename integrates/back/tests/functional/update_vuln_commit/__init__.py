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
    vuln_commit: str,
    vuln_id: str,
    vuln_where: str,
    vuln_specific: str,
) -> Dict[str, Any]:
    return await get_graphql_result(
        {
            "query": f"""
                mutation {{
                    updateVulnCommit(
                        vulnCommit: "{vuln_commit}"
                        vulnId: "{vuln_id}"
                        vulnWhere: "{vuln_where}"
                        vulnSpecific: "{vuln_specific}"
                    ){{
                        success
                    }}
                }}
            """,
        },
        stakeholder=stakeholder,
        context=get_new_context(),
    )
