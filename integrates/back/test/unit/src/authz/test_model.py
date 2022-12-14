import authz
from authz.model import (
    get_user_level_roles_model,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
    Set,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["parameter", "expected"],
    [
        (
            authz.GROUP_LEVEL_ROLES,
            [
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            ],
        ),
        (
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES,
            [
                "admin",
                "hacker",
                "user",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "hacker",
                "user",
            ],
        ),
        (
            authz.SERVICE_ATTRIBUTES,
            [
                "asm",
                "continuous",
                "forces",
                "report_vulnerabilities",
                "service_black",
                "service_white",
                "squad",
            ],
        ),
    ],
)
def test_model_integrity_keys_1(
    parameter: Dict[str, Any], expected: List[str]
) -> None:
    assert sorted(parameter.keys()) == expected


@pytest.mark.parametrize(
    ["parameter"],
    [
        [authz.GROUP_LEVEL_ROLES],
        [authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS],
        [authz.USER_LEVEL_ROLES],
        [authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS],
    ],
)
def test_model_integrity_keys_2(parameter: Dict[str, Any]) -> None:
    for value in parameter.values():
        assert sorted(value.keys()) == ["actions", "tags"]


@pytest.mark.parametrize(
    ["roles_common", "roles_fluid"],
    [
        (authz.GROUP_LEVEL_ROLES, authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS),
        (
            authz.ORGANIZATION_LEVEL_ROLES,
            authz.ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS,
        ),
        (authz.USER_LEVEL_ROLES, authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS),
    ],
)
def test_model_integrity_roles(
    roles_common: Dict[str, Any], roles_fluid: Dict[str, Any]
) -> None:
    assert sorted(roles_common.keys()) == sorted(roles_fluid.keys())


@pytest.mark.parametrize(
    ["email", "expected_output"],
    [
        [
            "continuoushacking@gmail.com",
            {
                "admin": {
                    "actions": {
                        "api_resolvers_query_list_user_groups_resolve",
                        "api_resolvers_query_vulnerabilities_to_reattack_resolve",  # noqa: E501
                        "api_resolvers_query_groups_with_forces_resolve",
                        "api_resolvers_query_groups_resolve",
                        "api_mutations_add_organization_mutate",
                        "api_mutations_update_stakeholder_phone_mutate",
                        "grant_user_level_role:hacker",
                        "api_mutations_start_machine_execution_mutate",
                        "api_mutations_add_group_mutate",
                        "grant_user_level_role:user",
                        "front_can_use_groups_searchbar",
                        "grant_user_level_role:admin",
                        "api_mutations_add_machine_execution_mutate",
                        "api_mutations_finish_machine_execution_mutate",
                        "api_mutations_submit_group_machine_execution_mutate",
                        "api_mutations_verify_stakeholder_mutate",
                        "api_mutations_add_stakeholder_mutate",
                    },
                    "tags": set(),
                },
                "hacker": {
                    "actions": {
                        "api_mutations_verify_stakeholder_mutate",
                        "api_mutations_update_stakeholder_phone_mutate",
                    },
                    "tags": {"drills"},
                },
                "user": {
                    "actions": {
                        "api_mutations_update_stakeholder_phone_mutate",
                        "api_mutations_verify_stakeholder_mutate",
                        "api_mutations_add_organization_mutate",
                    },
                    "tags": set(),
                },
            },
        ],
        [
            "integrateshacker@fluidattacks.com",
            {
                "admin": {
                    "actions": {
                        "api_resolvers_query_list_user_groups_resolve",
                        "api_resolvers_query_vulnerabilities_to_reattack_resolve",  # noqa: E501
                        "front_can_edit_credentials_secrets_in_bulk",
                        "api_resolvers_query_groups_with_forces_resolve",
                        "api_resolvers_query_groups_resolve",
                        "api_mutations_add_organization_mutate",
                        "front_can_retrieve_todo_drafts",
                        "front_can_retrieve_todo_events",
                        "api_mutations_update_stakeholder_phone_mutate",
                        "grant_user_level_role:hacker",
                        "front_can_retrieve_todo_reattacks",
                        "api_mutations_start_machine_execution_mutate",
                        "api_mutations_add_group_mutate",
                        "grant_user_level_role:user",
                        "front_can_use_groups_searchbar",
                        "grant_user_level_role:admin",
                        "api_mutations_add_machine_execution_mutate",
                        "api_mutations_finish_machine_execution_mutate",
                        "api_resolvers_finding_hacker_resolve",
                        "api_mutations_submit_group_machine_execution_mutate",
                        "api_mutations_verify_stakeholder_mutate",
                        "api_mutations_add_stakeholder_mutate",
                        "can_assign_vulnerabilities_to_fluidattacks_staff",
                    },
                    "tags": set(),
                },
                "hacker": {
                    "actions": {
                        "api_resolvers_query_list_user_groups_resolve",
                        "api_mutations_add_group_mutate",
                        "front_can_use_groups_searchbar",
                        "front_can_edit_credentials_secrets_in_bulk",
                        "api_mutations_add_organization_mutate",
                        "front_can_retrieve_todo_drafts",
                        "front_can_retrieve_todo_events",
                        "api_resolvers_finding_hacker_resolve",
                        "api_mutations_update_stakeholder_phone_mutate",
                        "front_can_retrieve_todo_reattacks",
                        "api_mutations_verify_stakeholder_mutate",
                        "can_assign_vulnerabilities_to_fluidattacks_staff",
                        "api_mutations_update_toe_lines_sorts_mutate",
                    },
                    "tags": {"drills"},
                },
                "user": {
                    "actions": {
                        "api_mutations_add_group_mutate",
                        "front_can_use_groups_searchbar",
                        "front_can_edit_credentials_secrets_in_bulk",
                        "api_mutations_add_organization_mutate",
                        "front_can_retrieve_todo_drafts",
                        "front_can_retrieve_todo_events",
                        "api_resolvers_finding_hacker_resolve",
                        "api_mutations_update_stakeholder_phone_mutate",
                        "front_can_retrieve_todo_reattacks",
                        "api_mutations_verify_stakeholder_mutate",
                        "can_assign_vulnerabilities_to_fluidattacks_staff",
                    },
                    "tags": set(),
                },
            },
        ],
    ],
)
def test_get_user_level_roles_model(
    email: str, expected_output: Dict[str, Dict[str, Set[str]]]
) -> None:
    assert get_user_level_roles_model(email) == expected_output
