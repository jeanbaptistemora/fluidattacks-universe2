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
