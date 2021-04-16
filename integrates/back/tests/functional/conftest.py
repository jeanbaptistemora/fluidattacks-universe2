# Standard libraries
from typing import (
    Any,
    Set,
    Dict,
)

# Third party libraries
import pytest

# Constants
TEST_GROUPS: Set[str] = {
    'add_event_consult',
    'add_files',
    'add_finding_consult',
    'add_git_root',
    'add_project_consult',
    'add_tags',
    'approve_draft',
    'create_draft',
    'create_event',
    'create_organization',
    'create_project',
    'delete_finding',
    'delete_vulnerability',
    'download_event_file',
    'download_vuln_file',
    'download_file',
    'edit_group',
    'edit_stakeholder',
    'edit_stakeholder_organization',
    'event',
    'events',
    'finding',
    'forces_executions',
    'grant_stakeholder_access',
    'grant_stakeholder_organization_access',
    'groups_with_forces',
    'internal_names',
    'old',
    'organization',
    'organization_id',
    'project',
    'reject_draft',
    'remove_event_evidence',
    'remove_evidence',
    'remove_files',
    'remove_group',
    'remove_stakeholder_access',
    'remove_stakeholder_organization_access',
    'remove_tag',
    'request_verification_vuln',
    'resources',
    'sign_in',
    'solve_event',
    'stakeholder',
    'submit_draft',
    'unsubscribe_from_group',
    'update_access_token',
    'update_event_evidence',
    'update_evidence',
    'update_evidence_description',
    'update_finding_description',
    'update_forces_access_token',
    'update_organization_policies',
    'update_severity',
    'upload_file',
    'verify_request_vuln',
    'vulnerability',
}

@pytest.fixture(autouse=True, scope='session')
def generic_data() -> Dict[str, Any]:
    return {
       'users': [
            {
                'email': 'admin@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'analyst@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'closer@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'customer@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'customeradmin@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'executive@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'resourcer@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'reviewer@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
       ],
       'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [],
                'groups': [
                    'group1',
                ],
                'policy': {},
            },
        ],
        'groups': [
            {
                'project_name': 'group1',
                'description': '-',
                'language': 'en',
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': True,
                    'has_forces': True,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
            },
        ],
        'policies': [
            {
                'level': 'user',
                'subject': 'admin@gmail.com',
                'object': 'self',
                'role': 'admin',
            },
            {
                'level': 'user',
                'subject': 'analyst@gmail.com',
                'object': 'self',
                'role': 'analyst',
            },
            {
                'level': 'user',
                'subject': 'closer@gmail.com',
                'object': 'self',
                'role': 'closer',
            },
            {
                'level': 'user',
                'subject': 'customer@gmail.com',
                'object': 'self',
                'role': 'customer',
            },
            {
                'level': 'user',
                'subject': 'customeradmin@gmail.com',
                'object': 'self',
                'role': 'customeradmin',
            },
            {
                'level': 'user',
                'subject': 'executive@gmail.com',
                'object': 'self',
                'role': 'executive',
            },
            {
                'level': 'user',
                'subject': 'resourcer@gmail.com',
                'object': 'self',
                'role': 'resourcer',
            },
            {
                'level': 'user',
                'subject': 'reviewer@gmail.com',
                'object': 'self',
                'role': 'reviewer',
            },
            {
                'level': 'group',
                'subject': 'analyst@gmail.com',
                'object': 'group1',
                'role': 'analyst',
            },
            {
                'level': 'group',
                'subject': 'closer@gmail.com',
                'object': 'group1',
                'role': 'closer',
            },
            {
                'level': 'group',
                'subject': 'customer@gmail.com',
                'object': 'group1',
                'role': 'customer',
            },
            {
                'level': 'group',
                'subject': 'customeradmin@gmail.com',
                'object': 'group1',
                'role': 'customeradmin',
            },
            {
                'level': 'group',
                'subject': 'executive@gmail.com',
                'object': 'group1',
                'role': 'executive',
            },
            {
                'level': 'group',
                'subject': 'resourcer@gmail.com',
                'object': 'group1',
                'role': 'resourcer',
            },
            {
                'level': 'group',
                'subject': 'reviewer@gmail.com',
                'object': 'group1',
                'role': 'reviewer',
            },
        ],
    }



def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        '--resolver-test-group',
        action='store',
        metavar='RESOLVER_TEST_GROUP',
    )


def pytest_runtest_setup(item: Any) -> None:
    resolver_test_group = item.config.getoption('--resolver-test-group')

    if not resolver_test_group:
        raise ValueError('resolver-test-group not specified')
    if resolver_test_group not in TEST_GROUPS:
        raise ValueError(
            f'resolver-test-group must be one of: {TEST_GROUPS}',
        )

    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name='resolver_test_group')
    }

    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f'resolver-test-group must be one of: {TEST_GROUPS}')

    if runnable_groups:
        if resolver_test_group not in runnable_groups:
            pytest.skip(f'Requires resolver test group in: {runnable_groups}')
