# Standard library
from typing import (
    Set,
    Tuple,
)

# Local libraries
from .enforcer import (
    get_group_level_enforcer,
    get_user_level_enforcer,
)
from .model import (
    ROLES
)


async def get_user_level_roles_a_user_can_grant(
    *,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = get_user_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in ROLES['user_level']
        if await enforcer(
            requester_email, 'self', f'grant_user_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


async def get_group_level_roles_a_user_can_grant(
    *,
    group: str,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = get_group_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in ROLES['group_level']
        if await enforcer(
            requester_email, group, f'grant_group_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


def get_group_level_roles_with_tag(tag: str) -> Set[str]:
    return {role for role, tags in ROLES['group_level'].items() if tag in tags}
