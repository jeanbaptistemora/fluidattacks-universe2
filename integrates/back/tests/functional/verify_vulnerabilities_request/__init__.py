from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    finding: str,
    vulnerability_id: str,
    status_after_verification: VulnerabilityStateStatus,
) -> Dict[str, Any]:
    open_vuln_ids = (
        f'["{vulnerability_id}"]'
        if status_after_verification == VulnerabilityStateStatus.OPEN
        else "[]"
    )
    closed_vuln_ids = (
        f'["{vulnerability_id}"]'
        if status_after_verification == VulnerabilityStateStatus.CLOSED
        else "[]"
    )
    query: str = f"""
        mutation {{
            verifyVulnerabilitiesRequest(
                findingId: "{finding}",
                justification: "Vuln verified",
                openVulnerabilities: {open_vuln_ids},
                closedVulnerabilities: {closed_vuln_ids}
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
