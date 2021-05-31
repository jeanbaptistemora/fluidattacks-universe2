# Standard library

# Third party libraries
import pytest

# Local libraries
import authz

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
                "continuous",
                "drills_black",
                "drills_white",
                "forces",
                "integrates",
            ],
        ),
    ],
)
def test_model_integrity_keys_1(parameter, expected):
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
def test_model_integrity_keys_2(parameter):
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
def test_model_integrity_roles(roles_common, roles_fluid):
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
    permission_name, permissions
):
    migrated_permissions = {
        "api_mutations_create_draft_mutate": "api_mutations_create_draft_new_mutate",
        "api_mutations_submit_draft_mutate": "api_mutations_submit_draft_mutate",
        "api_resolvers_finding_analyst_resolve": "api_resolvers_finding_new_analyst_new_resolve",
        "api_resolvers_finding_historic_state_resolve": "api_resolvers_finding_new_historic_state_new_resolve",
        "api_resolvers_finding_observations_resolve": "api_resolvers_finding_new_observations_new_resolve",
        "api_resolvers_finding_sorts_resolve": "api_resolvers_finding_new_sorts_new_resolve",
        "api_resolvers_finding_zero_risk_resolve": "api_resolvers_finding_new_zero_risk_new_resolve",
        "api_resolvers_query_finding_resolve": "api_resolvers_query_finding_new_resolve",
        "api_resolvers_query_finding__get_draft": "api_resolvers_query_finding_new__get_draft",
    }
    for role, value in permissions.items():
        for current_p, new_p in migrated_permissions.items():
            assert (current_p in value["actions"]) == (
                new_p in value["actions"]
            ), f"if {current_p} is included in the {role} actions for {permission_name} then {new_p} must be included"
