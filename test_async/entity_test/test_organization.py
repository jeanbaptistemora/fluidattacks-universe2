import pytest
from decimal import Decimal
from string import Template

from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
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


async def _get_result_async(data, user='integratesmanager@gmail.com'):
    """Get result."""
    request = create_dummy_session(username=user)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'project': ProjectLoader(),
        'vulnerability': VulnerabilityLoader()
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
async def test_edit_user_organization():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    user = 'org_testgroupmanager1@gmail.com'
    query = Template('''
        mutation {
            editUserOrganization(
                organizationId: "$org_id",
                phoneNumber: "-",
                role: $role,
                userEmail: "$user"
            ) {
                success
                modifiedUser {
                    email
                }
            }
        }
    ''')

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMER', user=user)}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['editUserOrganization']['success']
    assert result['data']['editUserOrganization']['modifiedUser']['email'] == user

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMERADMIN', user=user)}
    result = await _get_result_async(data, user=user)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(org_id=org_id, role='CUSTOMERADMIN', user='madeupuser@gmail.com')}
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_grant_user_organization_access():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    user = 'org_testuser5@gmail.com'
    query = Template(f'''
        mutation {{
            grantUserOrganizationAccess(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: $role,
                userEmail: "$user"
            ) {{
                success
                grantedUser {{
                    email
                }}
            }}
        }}
    ''')

    data = {'query': query.substitute(user=user, role='CUSTOMER')}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['grantUserOrganizationAccess']['success']
    assert result['data']['grantUserOrganizationAccess']['grantedUser']['email'] == user

    data = {'query': query.substitute(user='madeupuser@gmail.com', role='CUSTOMER')}
    result = await _get_result_async(data, user=user)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(user='madeupuser@gmail.com', role='CUSTOMER')}
    result = await _get_result_async(data, 'madeupuser@gmail.com')
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


@pytest.mark.changes_db
async def test_remove_user_organization_access():
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    user = 'org_testuser4@gmail.com'
    query = Template(f'''
        mutation {{
            removeUserOrganizationAccess(
                organizationId: "{org_id}",
                userEmail: "$user"
            ) {{
                success
            }}
        }}
    ''')

    data = {'query': query.substitute(user=user)}
    result = await _get_result_async(data)
    assert 'errors' not in result
    assert result['data']['removeUserOrganizationAccess']['success']

    data = {'query': query.substitute(user='org_testuser2@gmail.com')}
    result = await _get_result_async(data, user='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    data = {'query': query.substitute(user='madeupuser@gmail.com')}
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]


async def test_organization():
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    expected_groups = ['oneshottest', 'unittesting']
    expected_users = [
        'continuoushacking@gmail.com',
        'integratesmanager@gmail.com',
        'integratesuser@gmail.com'
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
                users {{
                    email
                }}
            }}
        }}
    '''

    data = {'query': query}
    result = await _get_result_async(data)
    groups = [group['name'] for group in result['data']['organization']['projects']]
    users = [user['email'] for user in result['data']['organization']['users']]

    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == Decimal('60')
    assert result['data']['organization']['maxAcceptanceSeverity'] == Decimal('10.0')
    assert result['data']['organization']['maxNumberAcceptations'] == Decimal('2')
    assert result['data']['organization']['minAcceptanceSeverity'] == Decimal('0.0')
    assert result['data']['organization']['name'] == 'imamura'
    assert sorted(groups) == expected_groups
    assert sorted(users) == expected_users

    exe = UserNotInOrganization()
    result = await _get_result_async(data, user='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
