import pytest

from back.tests.functional.utils import complete_register
from back.tests.functional.group_manager.utils import get_result
from custom_exceptions import StakeholderNotFound


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('old')
async def test_user():
    group_name = 'unittesting'
    stakeholder = 'stakeholder@fluidattacks.com'
    phone_number = '3453453453'
    responsibility = 'test'
    role = 'EXECUTIVE'
    query = f'''
        mutation {{
            grantStakeholderAccess (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}"
                projectName: "{group_name}",
                responsibility: "{responsibility}",
                role: {role}
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
    assert  result['data']['grantStakeholderAccess']['success']
    assert  result['data']['grantStakeholderAccess']['grantedStakeholder'] == {'email': stakeholder}
    assert await complete_register(stakeholder, group_name)

    query = f'''
        {{
            project(projectName: "{group_name}") {{
                stakeholders {{
                    email
                    role
                    responsibility
                    phoneNumber
                    firstLogin
                    lastLogin
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    group_stakeholders = result['data']['project']['stakeholders']
    new_granted_access_stakeholder = list(filter(
        lambda group_stakeholder: group_stakeholder['email'] == stakeholder,
        group_stakeholders
    ))[0]
    assert new_granted_access_stakeholder['firstLogin'] == ''
    assert new_granted_access_stakeholder['lastLogin'] == ''
    assert new_granted_access_stakeholder['phoneNumber'] == phone_number
    assert new_granted_access_stakeholder['responsibility'] == responsibility
    assert new_granted_access_stakeholder['role'] == role.lower()

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {{
                    name
                }}
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == role.lower()
    assert  result['data']['stakeholder']['responsibility'] == responsibility
    assert  result['data']['stakeholder']['phoneNumber'] == phone_number
    assert  result['data']['stakeholder']['firstLogin'] == ''
    assert  result['data']['stakeholder']['lastLogin'] == ''
    assert  result['data']['stakeholder']['projects'] == [{'name': group_name}]

    phone_number = '17364735'
    responsibility = 'edited'
    role = 'GROUP_MANAGER'
    query = f'''
        mutation {{
            editStakeholder (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}",
                projectName: "{group_name}"
                responsibility: "{responsibility}",
                role: {role}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {{
                    name
                }}
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == role.lower()
    assert  result['data']['stakeholder']['responsibility'] == responsibility
    assert  result['data']['stakeholder']['phoneNumber'] == phone_number
    assert  result['data']['stakeholder']['firstLogin'] == ''
    assert  result['data']['stakeholder']['lastLogin'] == ''
    assert  result['data']['stakeholder']['projects'] == [{'name': group_name}]

    role = 'ANALYST'
    query = f'''
        mutation {{
            editStakeholder (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}",
                projectName: "{group_name}"
                responsibility: "{responsibility}",
                role: {role}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == role.lower()

    role = 'CLOSER'
    query = f'''
        mutation {{
            editStakeholder (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}",
                projectName: "{group_name}"
                responsibility: "{responsibility}",
                role: {role}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == role.lower()

    role = 'RESOURCER'
    query = f'''
        mutation {{
            editStakeholder (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}",
                projectName: "{group_name}"
                responsibility: "{responsibility}",
                role: {role}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == role.lower()

    query = f'''
        mutation {{
            removeStakeholderAccess (
                projectName: "{group_name}",
                userEmail: "{stakeholder}"
            )
            {{
                removedEmail
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['removeStakeholderAccess']
    assert result['data']['removeStakeholderAccess']['removedEmail'] == stakeholder

    query = f'''
        query {{
            stakeholder(entity: PROJECT,
                projectName: "{group_name}",
                userEmail: "{stakeholder}"
            )
            {{
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {{
                    name
                }}
                __typename
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == str(StakeholderNotFound())
