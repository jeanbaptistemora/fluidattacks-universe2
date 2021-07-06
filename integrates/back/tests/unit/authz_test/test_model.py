import authz
import pytest
from typing import (
    Any,
    Dict,
    List,
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
                "analyst",
                "closer",
                "customer",
                "customeradmin",
                "executive",
                "group_manager",
                "resourcer",
                "reviewer",
                "service_forces",
            ],
        ),
        (
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "analyst",
                "closer",
                "customer",
                "customeradmin",
                "executive",
                "group_manager",
                "resourcer",
                "reviewer",
                "service_forces",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES,
            [
                "admin",
                "analyst",
                "customer",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "analyst",
                "customer",
            ],
        ),
        (
            authz.SERVICE_ATTRIBUTES,
            [
                "asm",
                "continuous",
                "forces",
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
    ["permission_name", "permissions"],
    [
        ["GROUP_LEVEL_ROLES", authz.GROUP_LEVEL_ROLES],
        [
            "GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS",
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
        ],
    ],
)
def test_model_integrity_migrated_finding_permissions(
    permission_name: str, permissions: Dict[str, Any]
) -> None:
    migrated_permissions = {
        "api_mutations_approve_draft_mutate": "api_mutations_"
        "approve_draft_new_mutate",
        "api_mutations_create_draft_mutate": "api_mutations_"
        "create_draft_new_mutate",
        "api_mutations_delete_finding_mutate": "api_mutations_"
        "delete_finding_new_mutate",
        "api_mutations_reject_draft_mutate": "api_mutations_"
        "reject_draft_new_mutate",
        "api_mutations_remove_finding_evidence_mutate": "api_mutations_"
        "remove_finding_evidence_new_mutate",
        "api_mutations_submit_draft_mutate": "api_mutations_"
        "submit_draft_new_mutate",
        "api_mutations_update_evidence_mutate": "api_mutations_"
        "update_evidence_new_mutate",
        "api_mutations_update_evidence_description_mutate": "api_mutations_"
        "update_evidence_description_new_mutate",
        "api_mutations_update_finding_description_mutate": "api_mutations_"
        "update_finding_description_new_mutate",
        "api_mutations_update_severity_mutate": "api_mutations_"
        "update_severity_new_mutate",
        "api_resolvers_finding_analyst_resolve": "api_resolvers_"
        "finding_new_analyst_new_resolve",
        "api_resolvers_finding_historic_state_resolve": "api_resolvers_"
        "finding_new_historic_state_new_resolve",
        "api_resolvers_finding_observations_resolve": "api_resolvers_"
        "finding_new_observations_new_resolve",
        "api_resolvers_finding_sorts_resolve": "api_resolvers_"
        "finding_new_sorts_new_resolve",
        "api_resolvers_finding_zero_risk_resolve": "api_resolvers_"
        "finding_new_zero_risk_new_resolve",
        "api_resolvers_query_finding_resolve": "api_resolvers_"
        "query_finding_new_resolve",
        "api_resolvers_query_finding__get_draft": "api_resolvers_"
        "query_finding_new__get_draft",
    }
    for role, value in permissions.items():
        for current_p, new_p in migrated_permissions.items():
            assert (current_p in value["actions"]) == (
                new_p in value["actions"]
            ), f"if {current_p} is included in the {role} "
            f"actions for {permission_name} then {new_p} must be included"
