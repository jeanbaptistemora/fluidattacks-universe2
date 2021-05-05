# Standard libraries
from typing import (
    Any,
    Dict,
)
import pytest

# Third party libraries
from ariadne import graphql

# Local libraries
from back.tests.unit.utils import create_dummy_session
from backend.api import apply_context_attrs
from backend.api.schema import SCHEMA
from custom_exceptions import (
    PolicyAlreadyHandled,
)
from organizations_finding_policies import domain as policies_domain


pytestmark = [
    pytest.mark.asyncio,
]


async def _get_result_async(
    data: Dict[str, Any],
    stakeholder: str = 'integratesmanager@gmail.com'
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=stakeholder)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


@pytest.mark.changes_db
async def test_handle_org_finding_policy_acceptation():
    org_name = 'okada'
    finding_name = 'F037. Fuga de información técnica'
    finding_id = '457497318'
    vulns_query = '''
        query GetFindingVulnInfo($findingId: String!) {
            finding(identifier: $findingId) {
                vulnerabilities(state: "open") {
                    historicTreatment {
                        user
                        treatment
                    }
                }
            }
        }
    '''
    vulns_data = {'query': vulns_query, 'variables': {'findingId': finding_id}}
    result = await _get_result_async(vulns_data)
    assert 'errors' not in result
    vulns = result['data']['finding']['vulnerabilities']
    assert vulns[0]['historicTreatment'][-1]['treatment'] == 'NEW'

    add_mutation = '''
        mutation AddOrgFindingPolicy($findingName: String! $orgName: String!) {
            addOrgFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    '''
    data = {
        'query': add_mutation,
        'variables': {'orgName': org_name, 'findingName': finding_name}
    }
    result = await _get_result_async(data, 'integratescustomer@gmail.com')
    assert 'errors' not in result
    assert result['data']['addOrgFindingPolicy']['success']

    approver_user = 'integratesuser@gmail.com'
    handle_mutation = '''
        mutation HandleOrgFindingPolicyAcceptation(
            $findingPolicyId: ID!
            $orgName: String!
            $status: OrganizationFindindPolicy!
        ) {
            handleOrgFindingPolicyAcceptation(
                findingPolicyId: $findingPolicyId
                organizationName: $orgName
                status: $status
            ) {
                success
            }
        }
    '''

    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.split('.')[0].lower(),
    )
    hande_acceptation_data = {
        'query': handle_mutation,
        'variables': {
            'findingPolicyId': finding_policy.id,
            'orgName': org_name,
            'status': 'APPROVED'
        }
    }

    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder=approver_user
    )    
    assert 'errors' not in result
    assert result['data']['handleOrgFindingPolicyAcceptation']['success']

    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder='integratescustomer@gmail.com'
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder=approver_user
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(PolicyAlreadyHandled())

    vulns_data = {'query': vulns_query, 'variables': {'findingId': finding_id}}
    result = await _get_result_async(vulns_data)
    assert 'errors' not in result
    vulns = result['data']['finding']['vulnerabilities']
    assert (
        vulns[0]['historicTreatment'][-1]['treatment'] == 'ACCEPTED_UNDEFINED'
    )
    assert vulns[0]['historicTreatment'][-1]['user'] == approver_user


@pytest.mark.changes_db
async def test_deactivate_org_finding_policy():
    org_name = 'okada'
    finding_name = 'F081. Ausencia de doble factor de autenticación'
    finding_id = '475041513'
    vulns_query = '''
        query GetFindingVulnInfo($findingId: String!) {
            finding(identifier: $findingId) {
                vulnerabilities(state: "open") {
                    historicTreatment {
                        user
                        treatment
                    }
                }
            }
        }
    '''
    vulns_data = {'query': vulns_query, 'variables': {'findingId': finding_id}}
    result = await _get_result_async(vulns_data)
    assert 'errors' not in result
    vulns = result['data']['finding']['vulnerabilities']
    assert vulns[0]['historicTreatment'][-1]['treatment'] == 'NEW'

    add_mutation = '''
        mutation AddOrgFindingPolicy($findingName: String! $orgName: String!) {
            addOrgFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    '''
    data = {
        'query': add_mutation,
        'variables': {'orgName': org_name, 'findingName': finding_name}
    }
    result = await _get_result_async(data, 'integratescustomer@gmail.com')
    assert 'errors' not in result
    assert result['data']['addOrgFindingPolicy']['success']

    approver_user = 'integratesuser@gmail.com'
    handle_mutation = '''
        mutation HandleOrgFindingPolicyAcceptation(
            $findingPolicyId: ID!
            $orgName: String!
            $status: OrganizationFindindPolicy!
        ) {
            handleOrgFindingPolicyAcceptation(
                findingPolicyId: $findingPolicyId
                organizationName: $orgName
                status: $status
            ) {
                success
            }
        }
    '''
    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.split('.')[0].lower(),
    )
    hande_acceptation_data = {
        'query': handle_mutation,
        'variables': {
            'findingPolicyId': finding_policy.id,
            'orgName': org_name,
            'status': 'APPROVED'
        }
    }
    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder=approver_user
    )    
    assert 'errors' not in result
    assert result['data']['handleOrgFindingPolicyAcceptation']['success']

    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder='integratescustomer@gmail.com'
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    result = await _get_result_async(
        hande_acceptation_data,
        stakeholder=approver_user
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(PolicyAlreadyHandled())

    vulns_data = {'query': vulns_query, 'variables': {'findingId': finding_id}}
    result = await _get_result_async(vulns_data)
    assert 'errors' not in result
    vulns = result['data']['finding']['vulnerabilities']
    assert (
        vulns[0]['historicTreatment'][-1]['treatment'] == 'ACCEPTED_UNDEFINED'
    )
    assert vulns[0]['historicTreatment'][-1]['user'] == approver_user

    deactivate_mutation = '''
        mutation DeactivateOrgFindingPolicy(
            $findingPolicyId: ID!
            $orgName: String!
        ) {
            deactivateOrgFindingPolicy(
                findingPolicyId: $findingPolicyId
                organizationName: $orgName
            ) {
                success
            }
        }
    '''
    deactivate_mutation_data = {
        'query': deactivate_mutation,
        'variables': {
            'findingPolicyId': finding_policy.id,
            'orgName': org_name,
        }
    }
    result = await _get_result_async(
        deactivate_mutation_data,
        stakeholder=approver_user
    )    
    assert 'errors' not in result
    assert result['data']['deactivateOrgFindingPolicy']['success']

    result = await _get_result_async(
        deactivate_mutation_data,
        stakeholder='integratescustomer@gmail.com'
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    result = await _get_result_async(
        deactivate_mutation_data,
        stakeholder=approver_user
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(PolicyAlreadyHandled())

    vulns_data = {'query': vulns_query, 'variables': {'findingId': finding_id}}
    result = await _get_result_async(vulns_data)
    assert 'errors' not in result
    vulns = result['data']['finding']['vulnerabilities']
    assert vulns[0]['historicTreatment'][-1]['treatment'] == 'NEW'
    assert vulns[0]['historicTreatment'][-1]['user'] == approver_user


@pytest.mark.changes_db
async def test_add_org_finding_policy():
    org_name = 'okada'
    fin_name = 'F031. Permisos excesivos'
    query = '''
        mutation AddOrgFindingPolicy(
            $findingName: String!
            $orgName: String!
        ) {
            addOrgFindingPolicy(
                findingName: $findingName
                organizationName: $orgName
            ) {
                success
            }
        }
    '''

    data = {
        'query': query,
        'variables': {'orgName': org_name, 'findingName': fin_name}
    }
    result = await _get_result_async(
        data,
        stakeholder='integratescustomer@gmail.com'
    )
    assert 'errors' not in result
    assert result['data']['addOrgFindingPolicy']['success']

    result = await _get_result_async(
        data,
        stakeholder='org_testuser5@gmail.com'
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'


async def test_get_org_finding_policies():
    id = '8b35ae2a-56a1-4f64-9da7-6a552683bf46'
    name = 'F007. Cross site request forgery'
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    status = 'APPROVED'
    query = '''
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
    '''
    data = {'query': query, 'variables': {'organizationId': org_id}}
    result = await _get_result_async(data)

    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert len(result['data']['organization']['findingPolicies']) == 1
    assert result['data']['organization']['findingPolicies'][0]['id'] == id
    assert result['data']['organization']['findingPolicies'][0]['name'] == name
    assert (
        result['data']['organization']['findingPolicies'][0]['status'] == status
    )
