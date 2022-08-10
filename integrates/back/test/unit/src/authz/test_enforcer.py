import authz
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from typing import (
    Any,
    Set,
    Tuple,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_group_level_enforcer() -> None:
    loaders: Dataloaders = get_new_context()
    test_cases = {
        # Common user, group
        ("test@tests.com", "test"),
        # Fluid user, group
        ("test@fluidattacks.com", "unittesting"),
    }
    for subject, group in test_cases:
        model = authz.get_group_level_roles_model(subject)

        for role in model:
            await authz.revoke_user_level_role(subject)
            await authz.revoke_group_level_role(subject, group)
            await authz.grant_group_level_role(loaders, subject, group, role)
            enforcer = await authz.get_group_level_enforcer(subject)

            for action in model[role]["actions"]:
                assert enforcer(
                    group, action
                ), f"{role} should be able to do {action}"

            for other_role in model:
                for action in (
                    model[other_role]["actions"] - model[role]["actions"]
                ):
                    assert not enforcer(
                        group, action
                    ), f"{role} should not be able to do {action}"


@pytest.mark.changes_db
async def test_user_level_enforcer() -> None:
    test_cases = {
        # Common user, object_
        ("test@tests.com", "self"),
        # Fluid user, object_
        ("test@fluidattacks.com", "self"),
    }
    for subject, object_ in test_cases:
        model = authz.get_user_level_roles_model(subject)

        for role in model:
            await authz.revoke_user_level_role(subject)
            await authz.grant_user_level_role(subject, role)
            enforcer = await authz.get_user_level_enforcer(subject)

            for action in model[role]["actions"]:
                assert enforcer(
                    object_, action
                ), f"{role} should be able to do {action}"

            for other_role in model:
                for action in (
                    model[other_role]["actions"] - model[role]["actions"]
                ):
                    assert not enforcer(
                        object_, action
                    ), f"{role} should not be able to do {action}"


async def test_group_service_attributes_enforcer() -> None:
    loaders: Dataloaders = get_new_context()
    # All attributes must be tested for this test to succeed
    # This prevents someone to add a new attribute without testing it

    attributes_remaining_to_test: Set[Tuple[str, Any]] = {
        (group_name, attr)
        for group_name in ("unittesting", "oneshottest")
        for attrs in authz.SERVICE_ATTRIBUTES.values()
        for attr in set(attrs).union({"non_existing_attribute"})
    }

    for group_name, attribute, result in [
        ("unittesting", "can_report_vulnerabilities", True),
        ("unittesting", "has_service_black", False),
        ("unittesting", "has_service_white", True),
        ("unittesting", "has_forces", True),
        ("unittesting", "has_asm", True),
        ("unittesting", "has_squad", True),
        ("unittesting", "is_continuous", True),
        ("unittesting", "is_fluidattacks_customer", True),
        ("unittesting", "must_only_have_fluidattacks_hackers", True),
        ("unittesting", "non_existing_attribute", False),
        ("oneshottest", "can_report_vulnerabilities", True),
        ("oneshottest", "has_asm", True),
        ("oneshottest", "has_service_black", True),
        ("oneshottest", "has_service_white", False),
        ("oneshottest", "has_forces", False),
        ("oneshottest", "has_squad", False),
        ("oneshottest", "is_continuous", False),
        ("oneshottest", "is_fluidattacks_customer", True),
        ("oneshottest", "must_only_have_fluidattacks_hackers", True),
        ("oneshottest", "non_existing_attribute", False),
    ]:
        enforcer = await authz.get_group_service_attributes_enforcer(
            await loaders.group.load(group_name)
        )

        assert (
            enforcer(attribute) == result
        ), f"{group_name} attribute: {attribute}, should have value {result}"

        attributes_remaining_to_test.remove((group_name, attribute))

    assert not attributes_remaining_to_test, (
        f"Please add tests for the following pairs of (group, attribute)"
        f": {attributes_remaining_to_test}"
    )
