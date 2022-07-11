import pytest
from typing import (
    Any,
    Set,
)

# Constants
TEST_GROUPS: Set[str] = {
    "test_client",
    "test_build_vulnerabilities_stream",
    "test_get_group_level_role",
    "test_bad_integrates_api_token",
    "test_should_execute_a_reattack",
    "test_reattack_comments_open_and_closed_vulnerability",
    "test_rebase_change_line_2",
    "test_rebase_change_line_3",
    "test_integrates_group_is_pristine_run",
    "test_integrates_group_is_pristine_check",
    "test_integrates_group_has_required_roots",
    "test_should_report_nothing_to_integrates_run",
    "test_should_report_nothing_to_integrates_verify",
    "test_should_report_vulns_to_namespace_run",
    "test_should_report_vulns_to_namespace_verify",
    "test_should_report_vulns_to_namespace2_run",
    "test_should_report_vulns_to_namespace2_verify",
    "test_should_close_vulns_to_namespace_run",
    "test_should_close_vulns_to_namespace_verify",
    "test_should_close_vulns_on_namespace2_run",
    "test_should_close_vulns_on_namespace2_verify",
}


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--resolver-test-group",
        action="store",
        metavar="RESOLVER_TEST_GROUP",
    )


def pytest_runtest_setup(item: Any) -> None:
    resolver_test_group = item.config.getoption("--resolver-test-group")

    if not resolver_test_group:
        raise ValueError("resolver-test-group not specified")
    if resolver_test_group not in TEST_GROUPS:
        raise ValueError(
            f"resolver-test-group must be one of: {TEST_GROUPS}",
        )

    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name="resolver_test_group")
    }

    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f"resolver-test-group must be one of: {TEST_GROUPS}")

    if runnable_groups and resolver_test_group not in runnable_groups:
        pytest.skip(f"Requires resolver test group in: {runnable_groups}")
