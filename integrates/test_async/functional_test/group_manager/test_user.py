import pytest

from test_async.functional_test.group_manager.utils import get_result

pytestmark = pytest.mark.asyncio


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
    assert  result['data']['stakeholder']['lastLogin'] == '[-1, -1]'
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
    assert  result['data']['stakeholder']['lastLogin'] == '[-1, -1]'
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
    assert 'errors' not in result
    assert  result['data']['stakeholder']['email'] == stakeholder
    assert  result['data']['stakeholder']['role'] == ''
    assert  result['data']['stakeholder']['responsibility'] == '-'
    assert  result['data']['stakeholder']['phoneNumber'] == phone_number
    assert  result['data']['stakeholder']['firstLogin'] == ''
    assert  result['data']['stakeholder']['lastLogin'] == '[-1, -1]'
    assert  result['data']['stakeholder']['projects'] == []
