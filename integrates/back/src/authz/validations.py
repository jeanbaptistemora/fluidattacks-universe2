# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .boundary import (
    get_group_level_roles_with_tag,
)
from .enforcer import (
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
)
from custom_exceptions import (
    InvalidCommentParent,
    InvalidUserProvided,
    PermissionDenied,
    UnexpectedUserRole,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)

# Constants
FLUIDATTACKS_EMAIL_SUFFIX = "@fluidattacks.com"


def validate_fluidattacks_staff_on_group(
    group: Group, email: str, role: str
) -> bool:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""
    enforcer = get_group_service_attributes_enforcer(group)

    is_user_at_fluidattacks: bool = email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    user_has_hacker_role: bool = role in get_group_level_roles_with_tag(
        "drills", email
    )

    group_must_only_have_fluidattacks_hackers: bool = enforcer(
        "must_only_have_fluidattacks_hackers"
    )

    if (
        group_must_only_have_fluidattacks_hackers
        and user_has_hacker_role
        and not is_user_at_fluidattacks
    ):
        raise UnexpectedUserRole(
            "Groups with any active Fluid Attacks service can "
            "only have Hackers provided by Fluid Attacks"
        )
    return True


async def validate_handle_comment_scope(
    loaders: Dataloaders,
    content: str,
    user_email: str,
    group_name: str,
    parent_comment: str,
) -> None:
    enforcer = await get_group_level_enforcer(loaders, user_email)
    if content.strip() in {"#external", "#internal"}:
        if not enforcer(group_name, "handle_comment_scope"):
            raise PermissionDenied()
        if parent_comment == "0":
            raise InvalidCommentParent()


def validate_role_fluid_reqs(email: str, role: str) -> bool:
    """Validates that new users belong to Fluid Attacks before granting them
    a restricted role"""
    restricted_roles = {"customer_manager"}
    if role not in restricted_roles or (
        role in restricted_roles and email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    ):
        return True
    raise InvalidUserProvided()
