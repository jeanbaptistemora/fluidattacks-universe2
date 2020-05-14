# Standard library
from typing import (
    Callable,
    Coroutine,
)

# Local libraries
from .policy import (
    get_cached_group_service_attributes_policies,
    get_cached_subject_policies,
)
from .model import (
    ACTIONS,
    SERVICE_ATTRIBUTES,
)


def get_user_level_enforcer(subject: str) -> Callable[[str, str, str], Coroutine]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)

    async def enforcer(r_subject: str, r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            p_level == 'user'
            and r_subject == p_subject
            and r_object == p_object
            and r_action in ACTIONS.get(p_role, set())
            for p_level, p_subject, p_object, p_role in policies
        )

        return should_grant_access

    return enforcer


def get_group_access_enforcer() -> Callable[[dict, str], Coroutine]:

    # If you are going to create a new enforcer do not follow this pattern
    #   use a policy based enforcer
    # see: get_user_level_enforcer or get_group_level_enforcer for examples
    async def enforcer(r_data: dict, r_object: str) -> bool:
        should_grant_access: bool = \
            r_data['role'] == 'admin' \
            or r_object.lower() in r_data['subscribed_projects']

        return should_grant_access

    return enforcer


def get_group_level_enforcer(subject: str) -> Callable[[str, str, str], Coroutine]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)

    async def enforcer(r_subject: str, r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_subject == p_subject
            and ((p_level == 'user' and p_role == 'admin') or
                 (p_level == 'group' and r_object == p_object))
            and r_action in ACTIONS.get(p_role, set())
            for p_level, p_subject, p_object, p_role in policies
        )

        return should_grant_access

    return enforcer


def get_group_service_attributes_enforcer(group: str) -> Callable[[str, str], Coroutine]:
    """Return a filtered group authorization for the provided group."""
    policies = get_cached_group_service_attributes_policies(group)

    async def enforcer(r_group: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_group == p_group
            and r_action in SERVICE_ATTRIBUTES[p_service]
            for p_group, p_service in policies
        )

        return should_grant_access

    return enforcer
