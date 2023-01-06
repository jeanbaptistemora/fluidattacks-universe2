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
    inactivity_period: int,
    max_acceptance_days: int,
    max_acceptance_severity: float,
    max_number_acceptances: int,
    min_acceptance_severity: float,
    min_breaking_severity: float,
    vulnerability_grace_period: int,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateOrganizationPolicies(
            $inactivityPeriod: Int
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
                inactivityPeriod: $inactivityPeriod
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
            "inactivityPeriod": inactivity_period,
            "maxAcceptanceDays": max_acceptance_days,
            "maxAcceptanceSeverity": max_acceptance_severity,
            "maxNumberAcceptances": max_number_acceptances,
            "minAcceptanceSeverity": min_acceptance_severity,
            "minBreakingSeverity": min_breaking_severity,
            "organizationId": organization_id,
            "organizationName": organization_name,
            "vulnerabilityGracePeriod": vulnerability_grace_period,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
