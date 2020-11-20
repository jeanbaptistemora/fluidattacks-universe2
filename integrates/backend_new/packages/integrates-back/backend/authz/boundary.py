# Standard library
import logging
from typing import (
    Set,
    Tuple,
)

from fluidintegrates.settings import LOGGING

# Local libraries
from .enforcer import (
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
    get_organization_level_enforcer,
    get_user_level_enforcer,
)
from .model import (
    GROUP_LEVEL_ACTIONS,
    GROUP_LEVEL_ROLES,
    ORGANIZATION_LEVEL_ACTIONS,
    SERVICE_ATTRIBUTES_SET,
    USER_LEVEL_ACTIONS,
    USER_LEVEL_ROLES,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_user_level_actions(
    subject: str,
    with_cache: bool = True
) -> Set[str]:
    enforcer = await get_user_level_enforcer(
        subject,
        with_cache=with_cache
    )
    object_ = 'self'

    user_actions = {
        action
        for action in USER_LEVEL_ACTIONS
        if enforcer(object_, action)
    }

    if not user_actions:
        LOGGER.error(
            'Empty user actions on get_user_level_actions',
            extra=dict(extra=locals())
        )

    return user_actions


async def get_user_level_roles_a_user_can_grant(
    *,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = await get_user_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in USER_LEVEL_ROLES
        if enforcer('self', f'grant_user_level_role:{role}')
    ])

    return roles_the_user_can_grant


async def get_group_level_actions(
    subject: str,
    group: str,
    with_cache: bool = True
) -> Set[str]:
    enforcer = await get_group_level_enforcer(
        subject,
        with_cache=with_cache
    )

    group_actions = {
        action
        for action in GROUP_LEVEL_ACTIONS
        if enforcer(group.lower(), action)
    }

    if not group_actions:
        LOGGER.error(
            'Empty group actions on get_group_level_actions',
            extra=dict(extra=locals())
        )

    return group_actions


async def get_organization_level_actions(
    subject: str,
    organization_id: str,
    with_cache: bool = True
) -> Set[str]:
    enforcer = await get_organization_level_enforcer(
        subject,
        with_cache=with_cache
    )

    organization_actions = {
        action
        for action in ORGANIZATION_LEVEL_ACTIONS
        if enforcer(organization_id.lower(), action)
    }

    if not organization_actions:
        LOGGER.error(
            'Empty organization actions on '
            'get_organization_level_actions',
            extra=dict(extra=locals())
        )

    return organization_actions


async def get_group_service_attributes(group: str) -> Set[str]:
    enforcer = await get_group_service_attributes_enforcer(group)

    return set(filter(enforcer, SERVICE_ATTRIBUTES_SET))


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
        if enforcer(group, f'grant_group_level_role:{role}')
    ])

    return roles_the_user_can_grant


def get_group_level_roles_with_tag(tag: str) -> Set[str]:
    return {
        role_name
        for role_name, role_definition in GROUP_LEVEL_ROLES.items()
        if tag in role_definition.get('tags', [])
    }
