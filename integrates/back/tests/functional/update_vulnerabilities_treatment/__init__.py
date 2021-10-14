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
    treatment: str,
) -> Dict[str, Any]:
    query = f"""
        mutation {{
            updateVulnerabilitiesTreatment(
                acceptanceDate: "2021-03-30 19:45:11",
                findingId: "{finding}",
                justification: "test of update vulns treatment justification",
                treatment: {treatment},
                treatmentManager: "customer@gmail.com",
                vulnerabilityId: "{vulnerability}"
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
