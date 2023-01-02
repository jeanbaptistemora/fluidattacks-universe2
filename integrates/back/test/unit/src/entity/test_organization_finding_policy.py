# pylint: disable=too-many-statements, import-error

from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
import asyncio
from back.test.unit.src.utils import (
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
    Dataloaders,
    get_new_context,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
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
    request = apply_context_attrs(request)  # type: ignore
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


async def _run(*, finding_policy_id: str) -> int:
    batch_action = await _get_batch_job(finding_policy_id=finding_policy_id)
    cmd_args: List[str] = [
        "test",
        batch_action.key,
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
                vulnerabilitiesConnection(state: OPEN) {
                    edges{
                        node{
                            tag
                            historicTreatment {
                                user
                                treatment
                            }
                        }
                    }
                }
            }
        }
    """
    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilitiesConnection"]
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["treatment"]
        == "NEW"
    )
    assert vulns["edges"][0]["node"]["tag"] == ""

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
    result = await _get_result_async(data, "integratesuser2@gmail.com")
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

    loaders: Dataloaders = get_new_context()
    finding_policy = await policies_domain.get_finding_policy_by_name(
        loaders=loaders,
        organization_name=org_name,
        finding_name=finding_name.lower(),
    )
    assert finding_policy is not None
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
    assert await _run(finding_policy_id=finding_policy.id) == 0

    result = await _get_result_async(
        hande_acceptance_data, stakeholder="integratesuser2@gmail.com"
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
    vulns = result["data"]["finding"]["vulnerabilitiesConnection"]
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["treatment"]
        == "ACCEPTED_UNDEFINED"
    )
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["user"]
        == approver_user
    )
    assert vulns["edges"][0]["node"]["tag"] == ", ".join(tags)


@pytest.mark.changes_db
async def test_deactivate_org_finding_policy() -> None:
    # pylint: disable=too-many-locals
    org_name = "okada"
    finding_name = "081. Lack of multi-factor authentication"
    finding_id = "475041513"
    vulns_query = """
        query GetFindingVulnInfo($findingId: String!) {
            finding(identifier: $findingId) {
                vulnerabilitiesConnection(state: OPEN) {
                    edges{
                        node{
                            tag
                            historicTreatment {
                                user
                                treatment
                            }
                        }
                    }
                }
            }
        }
    """
    vulns_data = {"query": vulns_query, "variables": {"findingId": finding_id}}
    result = await _get_result_async(vulns_data)
    assert "errors" not in result
    vulns = result["data"]["finding"]["vulnerabilitiesConnection"]
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["treatment"]
        == "NEW"
    )
    assert vulns["edges"][0]["node"]["tag"] == ""

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
    result = await _get_result_async(data, "integratesuser2@gmail.com")
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

    loaders: Dataloaders = get_new_context()
    finding_policy = await policies_domain.get_finding_policy_by_name(
        loaders=loaders,
        organization_name=org_name,
        finding_name=finding_name.lower(),
    )
    assert finding_policy is not None
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
    assert await _run(finding_policy_id=finding_policy.id) == 0

    result = await _get_result_async(
        hande_acceptance_data, stakeholder="integratesuser2@gmail.com"
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
    vulns = result["data"]["finding"]["vulnerabilitiesConnection"]
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["treatment"]
        == "ACCEPTED_UNDEFINED"
    )
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["user"]
        == approver_user
    )
    assert vulns["edges"][0]["node"]["tag"] == ""

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
    assert await _run(finding_policy_id=finding_policy.id) == 0

    result = await _get_result_async(
        deactivate_mutation_data, stakeholder="integratesuser2@gmail.com"
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
    vulns = result["data"]["finding"]["vulnerabilitiesConnection"]
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["treatment"]
        == "NEW"
    )
    assert (
        vulns["edges"][0]["node"]["historicTreatment"][-1]["user"]
        == approver_user
    )
    assert vulns["edges"][0]["node"]["tag"] == ""


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
        data, stakeholder="integratesuser2@gmail.com"
    )
    assert "errors" not in result
    assert result["data"]["addOrganizationFindingPolicy"]["success"]

    result = await _get_result_async(
        data, stakeholder="org_testuser5@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


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
        data, stakeholder="integratesuser2@gmail.com"
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

    loaders: Dataloaders = get_new_context()
    finding_policy = await policies_domain.get_finding_policy_by_name(
        loaders=loaders,
        organization_name=organization_name,
        finding_name=finding_name.lower(),
    )
    assert finding_policy is not None
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
        submit_finding_policy_data, stakeholder="integratesuser2@gmail.com"
    )
    assert "errors" not in result
    assert result["data"]["submitOrganizationFindingPolicy"]["success"]
    loaders = get_new_context()
    finding_policy_submitted: OrgFindingPolicy = (
        await loaders.organization_finding_policy.load(
            OrgFindingPolicyRequest(
                organization_name=organization_name,
                policy_id=finding_policy.id,
            )
        )
    )
    assert finding_policy_submitted.state.status == PolicyStateStatus.SUBMITTED
