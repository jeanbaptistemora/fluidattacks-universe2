# pylint: disable=import-error
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def put_mutation(
    *,
    user: str,
    finding: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
    acceptance_date: str,
) -> dict[str, Any]:
    query = """
        mutation UpdateTreatment(
            $findingId: String!,
            $treatment: UpdateClientDescriptionTreatment!,
            $assigned: String,
            $vulnerabilityId: ID!,
            $acceptanceDate: String,
        ) {
            updateVulnerabilitiesTreatment(
                acceptanceDate: $acceptanceDate,
                assigned: $assigned,
                findingId: $findingId,
                justification: "test of update vulns treatment justification",
                treatment: $treatment,
                vulnerabilityId: $vulnerabilityId
            ) {
            success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "acceptanceDate": acceptance_date,
            "findingId": finding,
            "treatment": treatment,
            "assigned": assigned,
            "vulnerabilityId": vulnerability,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_vulnerability(
    *,
    user: str,
    vulnerability_id: str,
) -> dict[str, Any]:
    query: str = """
        query GetVulnerability ($vulnerabilityId: String!) {
            vulnerability(uuid: $vulnerabilityId) {
                currentState
                historicTreatment{
                    assigned
                    date
                    treatment
                    treatmentManager
                }
                historicVerification{
                    date
                    status
                }
                id
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {"vulnerabilityId": vulnerability_id},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def grant_stakeholder(
    *,
    user: str,
    stakeholder: str,
    group: str,
    role: str = "USER",
) -> dict[str, Any]:
    query: str = """
        mutation GrantStakeholderGroupAccess(
            $stakeholder: String!
            $groupName: String!
            $role: StakeholderRole!
        ) {
            grantStakeholderAccess (
                email: $stakeholder
                groupName: $groupName
                role: $role
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "stakeholder": stakeholder,
            "groupName": group,
            "role": role,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_stakeholders(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = """
        query GetStakeholders($groupName: String!) {
            group (groupName: $groupName) {
                stakeholders {
                    email
                    invitationState
                }
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
