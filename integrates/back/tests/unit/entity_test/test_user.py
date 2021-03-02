from datetime import datetime, timedelta
import pytest

from ariadne import graphql, graphql_sync
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA
from back.tests.unit.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_user():
    """Check for user."""
    expected_output = {
        'email': 'continuoushacking@gmail.com',
        'role': 'customeradmin',
        'responsibility': 'Test',
        'phone_number': '-',
        'first_login': '2018-02-28 11:54:12',
        'last_login': '[186, 33677]',
        'projects':  [
             {'name': 'asgard'},
             {'name': 'barranquilla'},
             {'name': 'gotham'},
             {'name': 'metropolis'},
             {'name': 'monteria'},
             {'name': 'oneshottest'},
             {'name': 'unittesting'},
        ]

    }
    query = '''
        query {
            stakeholder(entity: PROJECT,
                    projectName: "unittesting",
                    userEmail: "continuoushacking@gmail.com") {
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {
                    name
                }
                __typename
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert result['data']['stakeholder']['email'] == expected_output.get('email')
    assert result['data']['stakeholder']['role'] == expected_output.get('role')
    assert result['data']['stakeholder']['responsibility'] == expected_output.get('responsibility')
    assert result['data']['stakeholder']['phoneNumber'] == expected_output.get('phone_number')
    assert result['data']['stakeholder']['firstLogin'] == expected_output.get('first_login')
    assert result['data']['stakeholder']['projects'] == expected_output.get('projects')
    assert 'stakeholder' in result['data']
    assert 'responsibility' in result['data']['stakeholder']
    assert 'phoneNumber' in result['data']['stakeholder']

async def test_user_list_projects():
    """Check for user."""
    query = '''
        query {
            userListProjects(userEmail: "continuoushacking@gmail.com") {
                name
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert result['data']['userListProjects'][0]['name'] == 'asgard'

@pytest.mark.changes_db
async def test_add_stakeholder():
    """Check for addStakeholder mutation."""
    query = '''
        mutation {
            addStakeholder(
                email: "test@test.com",
                role: CUSTOMER,
                phoneNumber: "3331112233"
            ) {
                success
                email
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session('integratesmanager@gmail.com')
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'addStakeholder' in result['data']
    assert 'success' in result['data']['addStakeholder']
    assert 'email' in result['data']['addStakeholder']

@pytest.mark.changes_db
async def test_grant_stakeholder_access_1():
    """Check for grantStakeholderAccess mutation."""
    query = '''
        mutation {
            grantStakeholderAccess (
            email: "test@test.test",
            phoneNumber: "3453453453"
            projectName: "unittesting",
            responsibility: "test",
            role: CUSTOMER) {
            success
            grantedStakeholder {
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
            }
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'success' in result['data']['grantStakeholderAccess']
    assert 'grantedStakeholder' in result['data']['grantStakeholderAccess']
    assert 'email' in result['data']['grantStakeholderAccess']['grantedStakeholder']

@pytest.mark.changes_db
async def test_grant_stakeholder_access_2():
    """Check for grantStakeholderAccess mutation."""
    query = '''
        mutation {
            grantStakeholderAccess (
            email: "test@test.test",
            phoneNumber: "3453453453"
            projectName: "unittesting",
            responsibility: "test",
            role: ANALYST) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    phoneNumber
                    firstLogin
                    lastLogin
                }
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' in result
    assert result['errors'][0]['message'] == (
        'Exception - Groups with any active Fluid Attacks service can '
        'only have Hackers provided by Fluid Attacks'
    )

@pytest.mark.changes_db
async def test_grant_stakeholder_access_3():
    """Check for grantStakeholderAccess mutation."""
    query = '''
        mutation {
            grantStakeholderAccess (
            email: "test@fluidattacks.com",
            phoneNumber: "3453453453"
            projectName: "unittesting",
            responsibility: "test",
            role: ANALYST) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    phoneNumber
                    firstLogin
                    lastLogin
                }
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'success' in result['data']['grantStakeholderAccess']
    assert 'grantedStakeholder' in result['data']['grantStakeholderAccess']
    assert 'email' in result['data']['grantStakeholderAccess']['grantedStakeholder']

@pytest.mark.changes_db
async def test_remove_stakeholder_access():
    """Check for removeStakeholderAccess mutation."""
    query = '''
        mutation {
            removeStakeholderAccess (
            projectName: "unittesting"
            userEmail: "test@test.test"
            )
            {
                removedEmail
                success
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'success' in result['data']['removeStakeholderAccess']
    assert 'removedEmail' in result['data']['removeStakeholderAccess']

@pytest.mark.changes_db
async def test_edit_stakeholder():
    """Check for editStakeholder mutation."""
    query = '''
        mutation {
            editStakeholder (
            email: "integratescustomer@gmail.com",
            phoneNumber: "17364735",
            projectName: "unittesting",
            responsibility: "edited",
            role: CUSTOMER) {
                success
            }
        }
    '''
    data = {'query': query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'success' in result['data']['editStakeholder']
