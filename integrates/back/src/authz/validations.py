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
from typing import (
    Any,
    DefaultDict,
)

# Constants
FLUIDATTACKS_EMAIL_SUFFIX = "@fluidattacks.com"


async def validate_fluidattacks_staff_on_group(
    group: str, email: str, role: str
) -> bool:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""
    enforcer = await get_group_service_attributes_enforcer(group)

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
    content: str,
    user_email: str,
    group_name: str,
    parent: str,
    context_store: DefaultDict[Any, Any] = DefaultDict(str),
) -> None:
    enforcer = await get_group_level_enforcer(user_email, context_store)
    if content.strip() in {"#external", "#internal"}:
        if not enforcer(group_name, "handle_comment_scope"):
            raise PermissionDenied()
        if parent == "0":
            raise InvalidCommentParent()


def validate_role_fluid_reqs(email: str, role: str) -> bool:
    """Validates that new users belong to Fluid Attacks before granting them
    a restricted role"""
    restricted_roles = {"system_owner", "group_manager"}
    if role not in restricted_roles or (
        role in restricted_roles and email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    ):
        return True
    raise InvalidUserProvided()
