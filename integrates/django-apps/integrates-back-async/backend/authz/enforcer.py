# Standard library
from collections import defaultdict
from typing import (
    Callable,
)

# Local libraries
from .policy import (
    get_cached_group_service_attributes_policies,
    get_cached_subject_policies,
)
from .model import (
    GROUP_LEVEL_ROLES,
    SERVICE_ATTRIBUTES,
    ORGANIZATION_LEVEL_ROLES,
    USER_LEVEL_ROLES,
)


async def get_user_level_enforcer(subject: str) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = await get_cached_subject_policies(subject)
    roles = USER_LEVEL_ROLES

    # Filter results as early as possible to save cycles in the enforcer
    policies = tuple(
        item
        for item in policies
        for p_level, *_ in [item]
        if p_level == 'user'
    )

    def enforcer(r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_object == p_object
            and r_action in roles.get(p_role, {}).get('actions', set())
            for _, p_object, p_role in policies
        )

        return should_grant_access

    return enforcer


async def get_group_level_enforcer(
    subject: str,
    context_store: defaultdict = None,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided subject.

    The argument `context_store` will be used to memoize round-trips.
    """
    policies = await get_cached_subject_policies(subject, context_store)
    roles = GROUP_LEVEL_ROLES

    def enforcer(r_object: str, r_action: str) -> bool:
        has_group_level: bool = any(
            p_level == 'group'
            and r_object == p_object
            for p_level, p_object, _ in policies
        )
        can_do: bool = any(
            p_level == 'group'
            and r_object == p_object
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, p_object, p_role in policies
        )
        is_an_admin: bool = any(
            p_level == 'user' and p_role == 'admin'
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, p_object, p_role in policies
        )
        should_grant_access: bool = (can_do if has_group_level
                                     else is_an_admin)

        return should_grant_access

    return enforcer


async def get_group_service_attributes_enforcer(
    group: str,
) -> Callable[[str], bool]:
    """Return a filtered group authorization for the provided group."""
    policies = await get_cached_group_service_attributes_policies(group)

    def enforcer(r_attribute: str) -> bool:
        should_grant_access: bool = any(
            r_attribute in SERVICE_ATTRIBUTES[p_service]
            for p_service in policies
        )

        return should_grant_access

    return enforcer


async def get_organization_level_enforcer(
    subject: str,
) -> Callable[[str, str], bool]:
    """
    Return a filtered organization-level authorization
    for the provided subject.
    """
    policies = await get_cached_subject_policies(subject)
    roles = ORGANIZATION_LEVEL_ROLES

    def enforcer(r_object: str, r_action: str) -> bool:
        has_organization_level: bool = any(
            p_level == 'organization'
            and r_object == p_object
            for p_level, p_object, _ in policies
        )
        can_do: bool = any(
            p_level == 'organization'
            and r_object == p_object
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, p_object, p_role in policies
        )
        is_an_admin: bool = any(
            p_level == 'user' and p_role == 'admin'
            for p_level, p_object, p_role in policies
        )
        should_grant_access: bool = (can_do if has_organization_level
                                     else is_an_admin)

        return should_grant_access

    return enforcer
