import pytest
from decimal import Decimal
from string import Template

from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.schema import SCHEMA
from backend.exceptions import (
    InvalidOrganization,
    UserNotInOrganization
)
from test_async.utils import create_dummy_session


# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def _get_result_async(data, stakeholder='integratesmanager@gmail.com'):
    """Get result."""
    request = await create_dummy_session(username=stakeholder)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'group': GroupLoader(),
        'finding_vulns': FindingVulnsLoader()
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result


@pytest.mark.changes_db
async def test_create_organization():
    mutation_tpl = Template('''
        mutation {
            createOrganization(name: "$name") {
                organization {
                    id
                    name
                }
                success
            }
        }
    ''')

    name = 'AKAME'
    data = {'query': mutation_tpl.substitute(name=name)}
    result = await _get_result_async(data)

    assert 'errors' not in result
    assert result['data']['createOrganization']['success']
    assert result['data']['createOrganization']['organization']['name'] == name.lower()
    assert result['data']['createOrganization']['organization']['id'].startswith('ORG')

    name = 'MADEUP-NAME'
    data = {'query': mutation_tpl.substitute(name=name)}
    exe = InvalidOrganization()
    result = await _get_result_async(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_edit_stakeholder_organization():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    stakeholder = 'org_testgroupmanager1@gmail.com'
    query = Template('''
        mutation {
            editStakeholderOrganization(
                organizationId: "$org_id",
                phoneNumber: "-",
                role: $role,
                userEmail: "$email"
            ) {
                success
                modifiedStakeholder {
                    email
                }
            }
        }
    ''')

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMER', email=stakeholder)}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['editStakeholderOrganization']['success']
    assert result['data']['editStakeholderOrganization']['modifiedStakeholder']['email'] == stakeholder

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMERADMIN', email=stakeholder)}
    result = await _get_result_async(data, stakeholder=stakeholder)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMERADMIN', email='madeupuser@gmail.com')}
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_grant_stakeholder_organization_access():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    stakeholder = 'org_testuser6@gmail.com'
    query = Template(f'''
        mutation {{
            grantStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: $role,
                userEmail: "$email"
            ) {{
                success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    ''')

    data = {'query': query.substitute(email=stakeholder, role='CUSTOMER')}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['grantStakeholderOrganizationAccess']['success']
    assert result['data']['grantStakeholderOrganizationAccess']['grantedStakeholder']['email'] == stakeholder

    data = {'query': query.substitute(email='madeupuser@gmail.com', role='CUSTOMER')}
    result = await _get_result_async(data, stakeholder=stakeholder)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(email='madeupuser@gmail.com', role='CUSTOMER')}
    result = await _get_result_async(data, 'madeupuser@gmail.com')
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_remove_stakeholder_organization_access():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    stakeholder = 'org_testuser4@gmail.com'
    query = Template(f'''
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                userEmail: "$email"
            ) {{
                success
            }}
        }}
    ''')

    data = {'query': query.substitute(email=stakeholder)}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['removeStakeholderOrganizationAccess']['success']

    data = {'query': query.substitute(email='org_testuser2@gmail.com')}
    result = await _get_result_async(data, stakeholder='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(email='madeupuser@gmail.com')}
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_update_organization_policies():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    org_name = 'hajime'
    query = f'''
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.5,
                maxNumberAcceptations: 3,
                minAcceptanceSeverity: 1.5,
                organizationId: "{org_id}",
                organizationName: "{org_name}"
            ) {{
                success
            }}
        }}
    '''

    data = {'query': query}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['updateOrganizationPolicies']['success']

    result = await _get_result_async(data, stakeholder='org_testuser5@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    result = await _get_result_async(data, stakeholder='madeupuser@gmail.com')
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


async def test_get_organization_id():
    org_name = 'okada'
    expected_org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    query = Template('''
        query {
            organizationId(organizationName: "$name") {
                id
            }
        }
    ''')

    data = {'query': query.substitute(name=org_name)}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] == expected_org_id

    result = await _get_result_async(data, stakeholder='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(name='madeup-name')}
    result = await _get_result_async(data)
    exe = InvalidOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


async def test_organization():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    expected_groups = ['oneshottest', 'unittesting']
    expected_stakeholders = [
        'continuoushack2@gmail.com',
        'continuoushacking@gmail.com',
        'integratesanalyst@fluidattacks.com',
        'integratescloser@fluidattacks.com',
        'integratescustomer@gmail.com',
        'integratesexecutive@gmail.com',
        'integratesinternalmanager@fluidattacks.com',
        'integratesmanager@gmail.com',
        'integratesresourcer@fluidattacks.com',
        'integratesreviewer@fluidattacks.com',
        'integratesserviceforces@gmail.com'
    ]
    query = f'''
        query {{
            organization(organizationId: "{org_id}") {{
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptations
                minAcceptanceSeverity
                name
                projects {{
                    name
                }}
                stakeholders(pageIndex: 1) {{
                    stakeholders {{
                        email
                    }}
                }}
            }}
        }}
    '''

    data = {'query': query}
    result = await _get_result_async(data)
    groups = [group['name'] for group in result['data']['organization']['projects']]
    stakeholders = [stakeholders['email'] for stakeholders in result['data']['organization']['stakeholders']['stakeholders']]

    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == Decimal('60')
    assert result['data']['organization']['maxAcceptanceSeverity'] == Decimal('10.0')
    assert result['data']['organization']['maxNumberAcceptations'] == Decimal('2')
    assert result['data']['organization']['minAcceptanceSeverity'] == Decimal('0.0')
    assert result['data']['organization']['name'] == 'okada'
    assert sorted(groups) == expected_groups
    assert sorted(stakeholders) == expected_stakeholders

    exe = UserNotInOrganization()
    result = await _get_result_async(data, stakeholder='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
