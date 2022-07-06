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
    user: str,
    organization_id: str,
    organization_name: str,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateOrganizationPolicies(
            $maxAcceptanceDays: Int
            $maxAcceptanceSeverity: Float
            $maxNumberAcceptances: Int
            $minAcceptanceSeverity: Float
            $minBreakingSeverity: Float
            $vulnerabilityGracePeriod: Int
            $organizationId: String!
            $organizationName: String!
        ) {
            updateOrganizationPolicies(
                maxAcceptanceDays: $maxAcceptanceDays
                maxAcceptanceSeverity: $maxAcceptanceSeverity
                maxNumberAcceptances: $maxNumberAcceptances
                minBreakingSeverity: $minBreakingSeverity
                minAcceptanceSeverity: $minAcceptanceSeverity
                vulnerabilityGracePeriod: $vulnerabilityGracePeriod
                organizationId: $organizationId
                organizationName: $organizationName
            ) {
                success
                __typename
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "maxAcceptanceDays": 5,
            "maxAcceptanceSeverity": 8.2,
            "maxNumberAcceptances": 3,
            "minAcceptanceSeverity": 0.0,
            "minBreakingSeverity": 5.7,
            "organizationId": organization_id,
            "organizationName": organization_name,
            "vulnerabilityGracePeriod": 1000,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
