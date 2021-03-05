# Standard libraries
from typing import (
    Any,
    Set,
)

# Third party libraries
import pytest

# Constants
TEST_GROUPS: Set[str] = {
    'create_organization',
    'edit_stakeholder_organization',
    'finding',
    'grant_stakeholder_organization_access',
    'groups_with_forces',
    'old',
    'organization_id',
    'update_organization_policies',
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
