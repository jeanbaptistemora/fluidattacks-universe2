# Standard library
from typing import (
    Set,
    Tuple,
)

# Local libraries
from .enforcer import (
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
    get_organization_level_enforcer,
    get_user_level_enforcer,
)
from .model import (
    GROUP_LEVEL_ROLES,
    ORGANIZATION_LEVEL_ROLES,
    SERVICE_ATTRIBUTES,
    USER_LEVEL_ROLES,
)


async def get_user_level_actions(subject: str) -> Set[str]:
    enforcer = await get_user_level_enforcer(subject)
    object_ = 'self'

    return set(tuple([
        action
        for role_definition in USER_LEVEL_ROLES.values()
        for action in role_definition['actions']
        if await enforcer(subject, object_, action)
    ]))


async def get_user_level_roles_a_user_can_grant(
    *,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = await get_user_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in USER_LEVEL_ROLES
        if await enforcer(
            requester_email, 'self', f'grant_user_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


async def get_group_level_actions(subject: str, group: str) -> Set[str]:
    enforcer = await get_group_level_enforcer(subject)

    return set(tuple([
        action
        for role_definition in GROUP_LEVEL_ROLES.values()
        for action in role_definition['actions']
        if await enforcer(subject, group.lower(), action)
    ]))


async def get_organization_level_actions(
        subject: str,
        organization_id: str) -> Set[str]:
    enforcer = await get_organization_level_enforcer(subject)

    return set(tuple([
        action
        for role_definition in ORGANIZATION_LEVEL_ROLES.values()
        for action in role_definition['actions']
        if await enforcer(subject, organization_id.lower(), action)
    ]))


async def get_group_service_attributes(group: str) -> Set[str]:
    enforcer = await get_group_service_attributes_enforcer(group)

    return set(tuple([
        attribute
        for attributes in SERVICE_ATTRIBUTES.values()
        for attribute in attributes
        if await enforcer(attribute)
    ]))


async def get_group_level_roles_a_user_can_grant(
    *,
    group: str,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = await get_group_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in GROUP_LEVEL_ROLES
        if await enforcer(
            requester_email, group, f'grant_group_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


def get_group_level_roles_with_tag(tag: str) -> Set[str]:
    return {
        role_name
        for role_name, role_definition in GROUP_LEVEL_ROLES.items()
        if tag in role_definition.get('tags', [])
    }
