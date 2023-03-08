from authz.validations import (
    validate_fluidattacks_staff_on_group,
    validate_fluidattacks_staff_on_group_deco,
    validate_handle_comment_scope,
    validate_handle_comment_scope_deco,
    validate_role_fluid_reqs,
    validate_role_fluid_reqs_deco,
)
from custom_exceptions import (
    InvalidUserProvided,
    PermissionDenied,
    UnexpectedUserRole,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from groups.domain import (
    get_group,
)
import pytest
from typing import (
    NamedTuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_fluidattacks_staff_on_group() -> None:

    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load("oneshottest")

    assert group
    assert validate_fluidattacks_staff_on_group(
        group, "test@fluidattacks.com", "hacker"
    )
    assert validate_fluidattacks_staff_on_group(
        group, "test@gmail.com", "user"
    )
    with pytest.raises(UnexpectedUserRole):
        validate_fluidattacks_staff_on_group(group, "test@gmail.com", "hacker")


async def test_validate_fluidattacks_staff_on_group_deco() -> None:

    loaders: Dataloaders = get_new_context()
    group = await get_group(loaders, "oneshottest")

    @validate_fluidattacks_staff_on_group_deco("group", "email", "role")
    def decorated_func(
        group: Group, email: str, role: str
    ) -> tuple[Group, str, str]:
        return (group, email, role)

    assert decorated_func(
        group=group,
        email="test@fluidattacks.com",
        role="hacker",
    )
    assert decorated_func(
        group=group,
        email="test@gmail.com",
        role="user",
    )
    with pytest.raises(UnexpectedUserRole):
        decorated_func(
            group=group,
            email="test@gmail.com",
            role="hacker",
        )

    class TestClass(NamedTuple):
        group: Group
        email: str
        role: str

    test_obj = TestClass(
        group=group, email="test@fluidattacks.com", role="hacker"
    )

    test_obj_fail = TestClass(
        group=group, email="test@gmail.com", role="hacker"
    )

    @validate_fluidattacks_staff_on_group_deco(
        "test_obj.group",
        "test_obj.email",
        "test_obj.role",
    )
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(UnexpectedUserRole):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_role_fluid_reqs() -> None:
    assert validate_role_fluid_reqs(email="test@gmail.com", role="hacker")
    assert validate_role_fluid_reqs(
        email="test@fluidattacks.com", role="customer_manager"
    )
    with pytest.raises(InvalidUserProvided):
        validate_role_fluid_reqs(
            email="test@gmail.com", role="customer_manager"
        )


def test_validate_role_fluid_reqs_deco() -> None:
    @validate_role_fluid_reqs_deco("email", "role")
    def decorated_func(email: str, role: str) -> str:
        return email + role

    assert decorated_func(email="test@gmail.com", role="hacker")
    assert decorated_func(
        email="test@fluidattacks.com", role="customer_manager"
    )
    with pytest.raises(InvalidUserProvided):
        decorated_func(email="test@gmail.com", role="customer_manager")


async def test_validate_handle_comment_scope() -> None:
    with pytest.raises(PermissionDenied):
        await validate_handle_comment_scope(
            loaders=get_new_context(),
            content="#internal",
            user_email="unittest@fluidattacks.com",
            group_name="unittesting",
            parent_comment="0",
        )


async def test_validate_handle_comment_scope_deco() -> None:
    @validate_handle_comment_scope_deco(
        "loaders", "content", "user_email", "group_name", "parent_comment"
    )
    async def decorator(
        loaders: Dataloaders,
        content: str,
        user_email: str,
        group_name: str,
        parent_comment: str,
    ) -> tuple:
        return (loaders, content, user_email, group_name, parent_comment)

    with pytest.raises(PermissionDenied):
        await decorator(
            loaders=get_new_context(),
            content="#internal",
            user_email="unittest@fluidattacks.com",
            group_name="unittesting",
            parent_comment="0",
        )
