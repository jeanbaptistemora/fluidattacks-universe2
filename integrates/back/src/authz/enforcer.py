from .model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
    SERVICE_ATTRIBUTES,
)
from .policy import (
    get_cached_group_service_policies,
    get_cached_subject_policies,
    get_user_level_role,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from typing import (
    Any,
    Callable,
)


async def get_group_level_enforcer(
    loaders: Any,
    email: str,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided email."""
    groups_access: tuple[
        GroupAccess, ...
    ] = await loaders.stakeholder_groups_access.load(email)
    roles = get_group_level_roles_model(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(r_object: str, r_action: str) -> bool:
        return any(
            # Regular user with a group policy set for the r_object
            r_object == access.group_name
            and access.role
            and r_action in roles.get(access.role, {}).get("actions", set())
            for access in groups_access
        ) or (
            # An admin
            user_level_role == "admin"
            and r_action in roles.get("admin", {}).get("actions", set())
        )

    return enforcer


async def get_group_service_attributes_enforcer(
    group: Group,
) -> Callable[[str], bool]:
    """Return a filtered group authorization for the provided group."""
    policies = await get_cached_group_service_policies(group)

    def enforcer(r_attribute: str) -> bool:
        should_grant_access: bool = any(
            r_attribute in SERVICE_ATTRIBUTES[p_service]
            for p_service in policies
        )
        return should_grant_access

    return enforcer


async def get_organization_level_enforcer(
    loaders: Any,
    email: str,
) -> Callable[[str, str], bool]:
    """
    Return a filtered organization-level authorization
    for the provided email.
    """
    orgs_access: tuple[
        OrganizationAccess, ...
    ] = await loaders.stakeholder_organizations_access.load(email)
    roles = get_organization_level_roles_model(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(r_object: str, r_action: str) -> bool:
        return any(
            # Regular user with an organization policy set for the r_object
            r_object == access.organization_id
            and access.role
            and r_action in roles.get(access.role, {}).get("actions", set())
            for access in orgs_access
        ) or (
            # An admin
            user_level_role == "admin"
            and r_action in roles.get("admin", {}).get("actions", set())
        )

    return enforcer


async def get_user_level_enforcer(
    subject: str,
    with_cache: bool = True,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = await get_cached_subject_policies(
        subject, with_cache=with_cache
    )
    roles = get_user_level_roles_model(subject)

    # Filter results as early as possible to save cycles in the enforcer
    policies = tuple(
        item
        for item in policies
        for p_level, *_ in [item]
        if p_level == "user"
    )

    def enforcer(r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_object == p_object
            and r_action in roles.get(p_role, {}).get("actions", set())
            for _, p_object, p_role in policies
        )
        return should_grant_access

    return enforcer
