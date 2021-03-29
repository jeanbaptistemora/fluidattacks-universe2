# Standard libraries
from typing import (
    Any,
    Set,
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
