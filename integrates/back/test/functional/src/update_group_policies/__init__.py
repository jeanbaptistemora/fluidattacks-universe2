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


async def update_group_policies(
    *,
    group_name: str,
    max_acceptance_days: int,
    max_acceptance_severity: float,
    max_number_acceptances: int,
    min_acceptance_severity: float,
    min_breaking_severity: float,
    user: str,
    vulnerability_grace_period: int,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateGroupPolicies(
            $groupName: String!
            $maxAcceptanceDays: Int
            $maxAcceptanceSeverity: Float
            $maxNumberAcceptances: Int
            $minAcceptanceSeverity: Float
            $minBreakingSeverity: Float
            $vulnerabilityGracePeriod: Int
        ) {
            updateGroupPolicies(
                groupName: $groupName
                maxAcceptanceDays: $maxAcceptanceDays
                maxAcceptanceSeverity: $maxAcceptanceSeverity
                maxNumberAcceptances: $maxNumberAcceptances
                minBreakingSeverity: $minBreakingSeverity
                minAcceptanceSeverity: $minAcceptanceSeverity
                vulnerabilityGracePeriod: $vulnerabilityGracePeriod
            ) {
                success
                __typename
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "maxAcceptanceDays": max_acceptance_days,
            "maxAcceptanceSeverity": max_acceptance_severity,
            "maxNumberAcceptances": max_number_acceptances,
            "minAcceptanceSeverity": min_acceptance_severity,
            "minBreakingSeverity": min_breaking_severity,
            "vulnerabilityGracePeriod": vulnerability_grace_period,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
