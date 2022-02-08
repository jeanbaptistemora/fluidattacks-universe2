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
                "architect",
                "customer",
                "customer_manager",
                "customeradmin",
                "executive",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
            ],
        ),
        (
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "architect",
                "customer",
                "customer_manager",
                "customeradmin",
                "executive",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES,
            [
                "admin",
                "customer",
                "hacker",
                "user",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "customer",
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
