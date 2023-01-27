from .model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
    SERVICE_ATTRIBUTES,
)
from .policy import (
    get_group_service_policies,
    get_user_level_role,
)
from dataloaders import (
    Dataloaders,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.groups.types import (
    Group,
)
from typing import (
    Callable,
)


async def get_group_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str, str], bool]:
    """Return a filtered group-level authorization for the provided email."""
    groups_access: tuple[
        GroupAccess, ...
    ] = await loaders.stakeholder_groups_access.load(email)
    roles = get_group_level_roles_model(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(group_name_to_test: str, action: str) -> bool:
        return any(
            # Regular user with a group policy set for the r_object
            group_name_to_test == access.group_name
            and access.role
            and action in roles.get(access.role, {}).get("actions", set())
            for access in groups_access
        ) or (
            # An admin
            user_level_role == "admin"
            and action in roles.get("admin", {}).get("actions", set())
        )

    return enforcer


def get_group_service_attributes_enforcer(
    group: Group,
) -> Callable[[str], bool]:
    """Return a filtered group authorization for the provided group."""
    policies = get_group_service_policies(group)

    def enforcer(r_attribute: str) -> bool:
        should_grant_access: bool = any(
            r_attribute in SERVICE_ATTRIBUTES[p_service]
            for p_service in policies
        )
        return should_grant_access

    return enforcer


async def get_organization_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str, str], bool]:
    """
    Return a filtered organization-level authorization
    for the provided email.
    """
    orgs_access = await loaders.stakeholder_organizations_access.load(email)
    roles = get_organization_level_roles_model(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(organization_id_to_test: str, action: str) -> bool:
        return any(
            # Regular user with an organization policy set for the r_object
            organization_id_to_test == access.organization_id
            and access.role
            and action in roles.get(access.role, {}).get("actions", set())
            for access in orgs_access
        ) or (
            # An admin
            user_level_role == "admin"
            and action in roles.get("admin", {}).get("actions", set())
        )

    return enforcer


async def get_user_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str], bool]:
    """Return a filtered group-level authorization for the provided email."""
    roles = get_user_level_roles_model(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(action: str) -> bool:
        return bool(
            user_level_role
            and action in roles.get(user_level_role, {}).get("actions", set())
        )

    return enforcer
