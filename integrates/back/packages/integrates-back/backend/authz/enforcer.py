# Standard library
from typing import (
    Any,
    Callable,
    DefaultDict
)

# Local libraries
from .policy import (
    get_cached_group_service_attributes_policies,
    get_cached_subject_policies,
)
from .model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
    SERVICE_ATTRIBUTES,
)


async def get_user_level_enforcer(
    subject: str,
    with_cache: bool = True,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = await get_cached_subject_policies(
        subject,
        with_cache=with_cache
    )
    roles = get_user_level_roles_model(subject)

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
    context_store: DefaultDict[Any, Any] = DefaultDict(str),
    with_cache: bool = True,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided subject.

    The argument `context_store` will be used to memoize round-trips.
    """
    policies = await get_cached_subject_policies(
        subject,
        context_store,
        with_cache=with_cache
    )
    roles = get_group_level_roles_model(subject)

    def enforcer(r_object: str, r_action: str) -> bool:
        return any(
            # Regular user with a group policy set for the r_object
            p_level == 'group'
            and r_object == p_object
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, p_object, p_role in policies
        ) or any(
            # An admin
            p_level == 'user'
            and p_role == 'admin'
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, _, p_role in policies
        )

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
    with_cache: bool = True,
) -> Callable[[str, str], bool]:
    """
    Return a filtered organization-level authorization
    for the provided subject.
    """
    policies = await get_cached_subject_policies(
        subject,
        with_cache=with_cache
    )
    roles = get_organization_level_roles_model(subject)

    def enforcer(r_object: str, r_action: str) -> bool:
        return any(
            # Regular user with an organization policy set for the r_object
            p_level == 'organization'
            and r_object == p_object
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, p_object, p_role in policies
        ) or any(
            # An admin
            p_level == 'user'
            and p_role == 'admin'
            and r_action in roles.get(p_role, {}).get('actions', set())
            for p_level, _, p_role in policies
        )

    return enforcer
