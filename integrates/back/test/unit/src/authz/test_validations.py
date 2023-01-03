from authz.validations import (
    validate_fluidattacks_staff_on_group_deco,
    validate_role_fluid_reqs_deco,
)
from custom_exceptions import (
    InvalidUserProvided,
    UnexpectedUserRole,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
import pytest
from typing import (
    Tuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_fluidattacks_staff_on_group_deco() -> None:

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group.load("oneshottest")

    @validate_fluidattacks_staff_on_group_deco("group", "email", "role")
    def decorated_func(
        group: Group, email: str, role: str
    ) -> Tuple[Group, str, str]:
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
