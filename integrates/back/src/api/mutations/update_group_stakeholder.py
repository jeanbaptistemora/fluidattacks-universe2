from .payloads.types import (
    UpdateStakeholderPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from authz.validations import (
    validate_fluidattacks_staff_on_group_deco,
    validate_role_fluid_reqs_deco,
)
from custom_exceptions import (
    InvalidRoleProvided,
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessRequest,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    exists,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
)
from newutils.utils import (
    map_roles,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)

# Constants
LOGGER = logging.getLogger(__name__)


@validate_fluidattacks_staff_on_group_deco(
    "group", "modified_email", "modified_role"
)
@validate_role_fluid_reqs_deco(
    email_field="modified_email", role_field="modified_role"
)
async def _update_stakeholder(
    *,
    info: GraphQLResolveInfo,
    updated_data: dict[str, str],
    modified_role: str,
    modified_email: str,
    group: Group,
) -> None:
    loaders: Dataloaders = info.context.loaders
    if not await exists(loaders, group.name, modified_email):
        raise StakeholderNotFound()

    group_access: GroupAccess = await loaders.group_access.load(
        GroupAccessRequest(group_name=group.name, email=modified_email)
    )
    invitation = group_access.invitation
    email = updated_data["email"]
    responsibility = updated_data["responsibility"]
    role = updated_data["role"]
    if invitation and not invitation.is_used:
        await stakeholders_domain.update_invited_stakeholder(
            loaders=loaders,
            email=email,
            responsibility=responsibility,
            role=role,
            invitation=invitation,
            group=group,
        )
    else:
        await authz.grant_group_level_role(
            loaders, modified_email, group.name, modified_role
        )
        await stakeholders_domain.update_information(
            info.context, updated_data, group.name
        )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    **updated_data: str,
) -> UpdateStakeholderPayload:
    group_name: str = updated_data["group_name"].lower()
    modified_role: str = map_roles(updated_data["role"])
    modified_email: str = updated_data["email"]
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(group_name)

    allowed_roles_to_grant = (
        await authz.get_group_level_roles_a_user_can_grant(
            loaders=loaders,
            group=group_name,
            requester_email=user_email,
        )
    )
    if modified_role not in allowed_roles_to_grant:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "modified_user_role": modified_role,
                    "group_name": group_name,
                    "requester_email": user_email,
                }
            },
        )
        raise InvalidRoleProvided(role=modified_role)

    await _update_stakeholder(
        info=info,
        updated_data=updated_data,
        modified_role=modified_role,
        modified_email=modified_email,
        group=group,
    )
    msg = (
        f"Security: Modified stakeholder data: {modified_email} "
        f"in {group_name} group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return UpdateStakeholderPayload(
        success=True,
        modified_stakeholder=dict(group_name=group_name, email=modified_email),
    )
