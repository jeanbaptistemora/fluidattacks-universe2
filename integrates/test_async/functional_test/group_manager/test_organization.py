import pytest
from decimal import Decimal

from backend.exceptions import UserNotInOrganization
from test_async.functional_test.group_manager.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_organization():
    org_name = 'OKADA'
    group_name = 'unittesting'
    org_id = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    stakeholder = 'org_testuser_3@gmail.com'
    stakeholder_role = 'CUSTOMER'
    query = f'''
        mutation {{
            grantStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
            ) {{
                success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['grantStakeholderOrganizationAccess']['success']
    assert result['data']['grantStakeholderOrganizationAccess']['grantedStakeholder']['email'] == stakeholder
    result = await get_result(data, stakeholder=stakeholder)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
    result = await get_result(data, stakeholder='madeupuser@gmail.com')
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

    phone_number = '9999999999'
    query = f'''
        mutation {{
            editStakeholderOrganization(
                organizationId: "{org_id}",
                phoneNumber: "{phone_number}",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
            ) {{
                success
                modifiedStakeholder {{
                    email

                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['editStakeholderOrganization']['success']
    assert result['data']['editStakeholderOrganization']['modifiedStakeholder']['email'] == stakeholder

    query = f'''
        query {{
            stakeholder(entity: ORGANIZATION,
                    organizationId: "{org_id}",
                    userEmail: "{stakeholder}") {{
                email
                projects{{
                    name
                }}
                phoneNumber
                role
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['stakeholder']['phoneNumber'] == phone_number

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
    result = await get_result(data)
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

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
                stakeholders {{
                    email
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    groups = [group['name'] for group in result['data']['organization']['projects']]
    stakeholders = [stakeholder['email'] for stakeholder in result['data']['organization']['stakeholders']]
    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == Decimal('5')
    assert result['data']['organization']['maxAcceptanceSeverity'] == Decimal('8.5')
    assert result['data']['organization']['maxNumberAcceptations'] == Decimal('3')
    assert result['data']['organization']['minAcceptanceSeverity'] == Decimal('1.5')
    assert result['data']['organization']['name'] == org_name.lower()
    assert group_name in groups
    assert stakeholder in stakeholders
    exe = UserNotInOrganization()
    result = await get_result(data, stakeholder='madeupuser@gmail.com')
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

    query = f'''
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                userEmail: "{stakeholder}"
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['removeStakeholderOrganizationAccess']['success']

    query = f'''
        query {{
            organization(organizationId: "{org_id}") {{
                stakeholders {{
                    email
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    stakeholders = [stakeholder['email'] for stakeholder in result['data']['organization']['stakeholders']]
    assert 'errors' not in result
    assert stakeholder not in stakeholders
