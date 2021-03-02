from decimal import Decimal
import pytest

# Local libraries
from backend.api import get_new_context
from backend.exceptions import (
    InvalidOrganization,
    UserNotInOrganization,
)
from back.tests.functional.admin.utils import get_result


@pytest.mark.asyncio
@pytest.mark.old
async def test_organization():
    context = get_new_context()
    org_name = 'AKAME'
    query = f'''
        mutation {{
            createOrganization(name: "{org_name}") {{
                organization {{
                    id
                    name
                }}
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['createOrganization']['success']
    assert result['data']['createOrganization']['organization']['name'] == org_name.lower()
    assert result['data']['createOrganization']['organization']['id'].startswith('ORG')
    org_id = result['data']['createOrganization']['organization']['id']
    data = {'query': query}
    result = await get_result(data, context=context)
    exe = InvalidOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

    context = get_new_context()
    stakeholder = 'org_testuser@gmail.com'
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
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['grantStakeholderOrganizationAccess']['success']
    assert result['data']['grantStakeholderOrganizationAccess']['grantedStakeholder']['email'] == stakeholder
    result = await get_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
    result = await get_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

    context = get_new_context()
    query = f'''
        mutation {{
            editStakeholderOrganization(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
            ) {{
                success
                modifiedStakeholder {{
                    email
                    phoneNumber
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['editStakeholderOrganization']['success']
    assert result['data']['editStakeholderOrganization']['modifiedStakeholder']['email'] == stakeholder

    context = get_new_context()
    query = f'''
        query {{
            organizationId(organizationName: "{org_name}") {{
                id
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] == org_id
    result = await get_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' not in result
    assert result['data']['organizationId']['id'] == org_id

    context = get_new_context()
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
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['updateOrganizationPolicies']['success']
    result = await get_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
    result = await get_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    exe = UserNotInOrganization()
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]
    expected_groups = []
    expected_stakeholders = [
        'integratesmanager@gmail.com',
        stakeholder,
    ]

    context = get_new_context()
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
    result = await get_result(data, context=context)
    groups = [group['name'] for group in result['data']['organization']['projects']]
    stakeholders = [stakeholder['email'] for stakeholder in result['data']['organization']['stakeholders']]
    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == Decimal('5')
    assert result['data']['organization']['maxAcceptanceSeverity'] == Decimal('8.5')
    assert result['data']['organization']['maxNumberAcceptations'] == Decimal('3')
    assert result['data']['organization']['minAcceptanceSeverity'] == Decimal('1.5')
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == expected_groups
    assert sorted(stakeholders) == expected_stakeholders
    result = await get_result(data, stakeholder=stakeholder, context=context)
    groups = [group['name'] for group in result['data']['organization']['projects']]
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == Decimal('5')
    assert result['data']['organization']['maxAcceptanceSeverity'] == Decimal('8.5')
    assert result['data']['organization']['maxNumberAcceptations'] == Decimal('3')
    assert result['data']['organization']['minAcceptanceSeverity'] == Decimal('1.5')
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == expected_groups
    exe = UserNotInOrganization()
    result = await get_result(
        data,
        stakeholder='madeupuser@gmail.com',
        context=context
    )
    assert 'errors' in result
    assert result['errors'][0]['message'] == exe.args[0]

    context = get_new_context()
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
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert result['data']['removeStakeholderOrganizationAccess']['success']

    context = get_new_context()
    query = f'''
        query {{
            organizationId(organizationName: "{org_name}") {{
                id
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
    assert result['data']['organizationId'] == None

    context = get_new_context()
    query = f'''
        query {{
            organization(organizationId: "{org_id}") {{
                id
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder=stakeholder, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'
    assert result['data']['organization'] == None
