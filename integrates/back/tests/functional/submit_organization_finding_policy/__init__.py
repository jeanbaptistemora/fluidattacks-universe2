# pylint: disable=import-error
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
    email: str,
    organization_name: str,
    finding_policy_id: str,
) -> Dict[str, Any]:
    mutation: str = f"""
        mutation {{
            submitOrganizationFindingPolicy(
                findingPolicyId: "{finding_policy_id}",
                organizationName: "{organization_name}",
            ) {{
                success
            }}
        }}
    """
    data = {"query": mutation}

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
