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
