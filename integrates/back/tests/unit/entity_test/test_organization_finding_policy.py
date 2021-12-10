# pylint: disable=too-many-statements
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
import asyncio
from back.tests.unit.utils import (
    create_dummy_session,
)
from batch.dal import (
    get_actions,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    PolicyAlreadyHandled,
)
from dataloaders import (
    apply_context_attrs,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from os import (
    environ,
)
import pytest
import subprocess
from typing import (
    Any,
    Dict,
    List,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def _get_result_async(
    data: Dict[str, Any], stakeholder: str = "integratesmanager@gmail.com"
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=stakeholder)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


async def _get_batch_job(*, finding_policy_id: str) -> BatchProcessing:
    all_actions = await get_actions()
    return next(
        (
            action
            for action in all_actions
            if action.entity == finding_policy_id
        )
    )


async def _run(
    *, finding_policy_id: str, org_name: str, user_email: str
) -> int:
    batch_action = await _get_batch_job(finding_policy_id=finding_policy_id)
    cmd_args: List[str] = [
        "test",
        "handle_finding_policy",
        finding_policy_id,
        user_email,
        batch_action.time,
        org_name,
    ]
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        environ["BATCH_BIN"],
        *cmd_args,
        stdin=subprocess.DEVNULL,
    )

    return await process.wait()


@pytest.mark.changes_db
async def test_handle_organization_finding_policy_acceptance() -> None:
    org_name = "okada"
    finding_name = "037. Technical information leak"
    finding_id = "457497318"
    vulns_query = """
        query GetFindingVulnInfo($findingId: String!) {
            finding(identifier: $findingId) {
                vulnerabilities(state: "open") {
                    tag
                    historicTreatment {
                        user
                        treatment
                    }
                }
            }
        }
    """
    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilities"]
    assert vulns[0]["historicTreatment"][-1]["treatment"] == "NEW"
    assert vulns[0]["tag"] == ""

    tags = ["password", "session"]
    add_mutation = """
        mutation AddOrganizationFindingPolicy(
            $findingName: String!
            $orgName: String!
            $tags: [String]
        ) {
            addOrganizationFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
                tags: $tags
            ) {
                success
            }
        }
    """
    data = {
        "query": add_mutation,
        "variables": {
            "orgName": org_name,
            "findingName": finding_name,
            "tags": tags,
        },
    }
    result = await _get_result_async(data, "integratescustomer@gmail.com")
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]

    approver_user = "integratesuser@gmail.com"
    handle_mutation = """
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

    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.lower(),
    )
    hande_acceptance_data = {
        "query": handle_mutation,
        "variables": {
            "findingPolicyId": finding_policy.id,
            "orgName": org_name,
            "status": "APPROVED",
        },
    }

    result = await _get_result_async(
        hande_acceptance_data, stakeholder=approver_user
    )
    assert "errors" not in result
    assert result["data"]["handleOrganizationFindingPolicyAcceptance"][
        "success"
    ]
    assert (
        await _run(
            finding_policy_id=finding_policy.id,
            org_name=org_name,
            user_email=approver_user,
        )
        == 0
    )

    result = await _get_result_async(
        hande_acceptance_data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
    result = await _get_result_async(
        hande_acceptance_data, stakeholder=approver_user
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(PolicyAlreadyHandled())

    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilities"]
    assert (
        vulns[0]["historicTreatment"][-1]["treatment"] == "ACCEPTED_UNDEFINED"
    )
    assert vulns[0]["historicTreatment"][-1]["user"] == approver_user
    assert vulns[0]["tag"] == ", ".join(tags)


@pytest.mark.changes_db
async def test_deactivate_org_finding_policy() -> None:
    org_name = "okada"
    finding_name = "081. Lack of multi-factor authentication"
    finding_id = "475041513"
    vulns_query = """
        query GetFindingVulnInfo($findingId: String!) {
            finding(identifier: $findingId) {
                vulnerabilities(state: "open") {
                    tag
                    historicTreatment {
                        user
                        treatment
                    }
                }
            }
        }
    """
    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilities"]
    assert vulns[0]["historicTreatment"][-1]["treatment"] == "NEW"
    assert vulns[0]["tag"] == ""

    add_mutation = """
        mutation AddOrganizationFindingPolicy(
            $findingName: String!
            $orgName: String!
            ) {
            addOrganizationFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    """
    data = {
        "query": add_mutation,
        "variables": {"orgName": org_name, "findingName": finding_name},
    }
    result = await _get_result_async(data, "integratescustomer@gmail.com")
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]

    approver_user = "integratesuser@gmail.com"
    handle_mutation = """
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
    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.lower(),
    )
    hande_acceptance_data = {
        "query": handle_mutation,
        "variables": {
            "findingPolicyId": finding_policy.id,
            "orgName": org_name,
            "status": "APPROVED",
        },
    }
    result = await _get_result_async(
        hande_acceptance_data, stakeholder=approver_user
    )
    assert "errors" not in result
    assert result["data"]["handleOrganizationFindingPolicyAcceptance"][
        "success"
    ]
    assert (
        await _run(
            finding_policy_id=finding_policy.id,
            org_name=org_name,
            user_email=approver_user,
        )
        == 0
    )

    result = await _get_result_async(
        hande_acceptance_data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    result = await _get_result_async(
        hande_acceptance_data, stakeholder=approver_user
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(PolicyAlreadyHandled())

    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilities"]
    assert (
        vulns[0]["historicTreatment"][-1]["treatment"] == "ACCEPTED_UNDEFINED"
    )
    assert vulns[0]["historicTreatment"][-1]["user"] == approver_user
    assert vulns[0]["tag"] == ""

    deactivate_mutation = """
        mutation DeactivateOrganizationFindingPolicy(
            $findingPolicyId: ID!
            $orgName: String!
        ) {
            deactivateOrganizationFindingPolicy(
                findingPolicyId: $findingPolicyId
                organizationName: $orgName
            ) {
                success
            }
        }
    """
    deactivate_mutation_data = {
        "query": deactivate_mutation,
        "variables": {
            "findingPolicyId": finding_policy.id,
            "orgName": org_name,
        },
    }
    result = await _get_result_async(
        deactivate_mutation_data, stakeholder=approver_user
    )
    assert "errors" not in result
    assert result["data"]["deactivateOrganizationFindingPolicy"]["success"]
    assert (
        await _run(
            finding_policy_id=finding_policy.id,
            org_name=org_name,
            user_email=approver_user,
        )
        == 0
    )

    result = await _get_result_async(
        deactivate_mutation_data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    result = await _get_result_async(
        deactivate_mutation_data, stakeholder=approver_user
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(PolicyAlreadyHandled())

    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilities"]
    assert vulns[0]["historicTreatment"][-1]["treatment"] == "NEW"
    assert vulns[0]["historicTreatment"][-1]["user"] == approver_user
    assert vulns[0]["tag"] == ""


@pytest.mark.changes_db
async def test_add_org_finding_policy() -> None:
    org_name = "okada"
    fin_name = "031. Excessive privileges - AWS"
    query = """
        mutation AddOrganizationFindingPolicy(
            $findingName: String!
            $orgName: String!
        ) {
            addOrganizationFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    """

    data = {
        "query": query,
        "variables": {"orgName": org_name, "findingName": fin_name},
    }
    result = await _get_result_async(
        data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]

    result = await _get_result_async(
        data, stakeholder="org_testuser5@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


async def test_get_org_finding_policies() -> None:
    identifier = "8b35ae2a-56a1-4f64-9da7-6a552683bf46"
    name = "007. Cross-site request forgery"
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    status = "APPROVED"
    query = """
        query GetOrganizationPolicies($organizationId: String!) {
            organization(organizationId: $organizationId) {
                id
                findingPolicies {
                    id
                    name
                    status
                    lastStatusUpdate
                }
            }
        }
    """
    data = {"query": query, "variables": {"organizationId": org_id}}
    result = await _get_result_async(data)

    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert len(result["data"]["organization"]["findingPolicies"]) == 1
    assert (
        result["data"]["organization"]["findingPolicies"][0]["id"]
        == identifier
    )
    assert result["data"]["organization"]["findingPolicies"][0]["name"] == name
    assert (
        result["data"]["organization"]["findingPolicies"][0]["status"]
        == status
    )


@pytest.mark.changes_db
async def test_submit_organization_finding_policy() -> None:
    organization_name = "okada"
    finding_name = "001. SQL injection - C Sharp SQL API"
    query = """
        mutation AddOrganizationFindingPolicy(
            $findingName: String!
            $orgName: String!
        ) {
            addOrganizationFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    """
    data = {
        "query": query,
        "variables": {
            "orgName": organization_name,
            "findingName": finding_name,
        },
    }
    result = await _get_result_async(
        data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]

    approver_user = "integratesuser@gmail.com"
    handle_mutation = """
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
    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=organization_name,
        finding_name=finding_name.lower(),
    )
    hande_acceptance_rejected_data = {
        "query": handle_mutation,
        "variables": {
            "findingPolicyId": finding_policy.id,
            "orgName": organization_name,
            "status": "REJECTED",
        },
    }
    result = await _get_result_async(
        hande_acceptance_rejected_data, stakeholder=approver_user
    )
    assert "errors" not in result
    assert result["data"]["handleOrganizationFindingPolicyAcceptance"][
        "success"
    ]

    submit_mutation = """
        mutation SubmitOrganizationFindingPolicy(
            $organizationName: String!
            $findingPolicyId: ID!
        ) {
            submitOrganizationFindingPolicy(
                findingPolicyId: $findingPolicyId
                organizationName: $organizationName
            ) {
                success
            }
        }
    """
    submit_finding_policy_data = {
        "query": submit_mutation,
        "variables": {
            "findingPolicyId": finding_policy.id,
            "organizationName": organization_name,
        },
    }
    result = await _get_result_async(
        submit_finding_policy_data, stakeholder="integratescustomer@gmail.com"
    )
    assert "errors" not in result
    assert result["data"]["submitOrganizationFindingPolicy"]["success"]
    finding_policy = await policies_domain.get_finding_policy(
        org_name=organization_name, finding_policy_id=finding_policy.id
    )
    assert finding_policy.state.status == "SUBMITTED"
