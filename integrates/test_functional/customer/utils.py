from test_functional.utils import (
    get_graphql_result,
    complete_register,
)

MANAGER = 'integratesmanager@gmail.com'
CUSTOMER = 'integratescustomer@gmail.com'


async def get_result(data, stakeholder='integratescustomer@gmail.com', session_jwt=None):
    """Get result for customer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt)
    return result


async def create_group():
    query = '''{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }'''
    data = {'query': query}
    result = await get_result(data, stakeholder=MANAGER)
    assert 'errors' not in result
    assert 'internalNames' in result['data']
    group_name = result['data']['internalNames']['name']

    org_name = 'okada'
    query = f'''
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "This is a new project from pytest",
                projectName: "{group_name}",
                subscription: CONTINUOUS,
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data, stakeholder=MANAGER)
    assert 'success' in result['data']['createProject']
    assert result['data']['createProject']['success']

    role = 'CUSTOMER'
    customer_email = CUSTOMER
    query = f'''
        mutation {{
            grantStakeholderAccess (
                email: "{customer_email}",
                phoneNumber: "-",
                projectName: "{group_name}",
                responsibility: "Customer",
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
    result = await get_result(data, stakeholder=MANAGER)
    assert 'errors' not in result
    assert result['data']['grantStakeholderAccess']['success']
    assert await complete_register(customer_email, group_name)

    return group_name
