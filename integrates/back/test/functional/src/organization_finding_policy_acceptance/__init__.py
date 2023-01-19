# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    email: str,
    organization_name: str,
    finding_policy_id: str,
    status: str,
) -> dict[str, Any]:
    mutation: str = """
        mutation handleOrganizationFindingPolicyAcceptance(
            $findingPolicyId: ID!
            $orgName: String!
            $status: OrganizationFindingPolicy!
        ) {
            handleOrganizationFindingPolicyAcceptance(
                findingPolicyId: $findingPolicyId
                organizationName: $orgName
                status: $status
            ) {
                success
            }
        }
    """
    data = {
        "query": mutation,
        "variables": {
            "findingPolicyId": finding_policy_id,
            "orgName": organization_name,
            "status": status,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
