from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_types import (
    UpdateStakeholderPayload as UpdateStakeholderPayloadType,
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
    token as token_utils,
)
from newutils.utils import (
    map_roles,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Dict,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _update_stakeholder(
    info: GraphQLResolveInfo,
    updated_data: Dict[str, str],
    group: Group,
) -> None:
    loaders: Dataloaders = info.context.loaders
    modified_role = map_roles(updated_data["role"])
    modified_email = updated_data["email"]

    if not await exists(loaders, group.name, modified_email):
        raise StakeholderNotFound()

    group_access: GroupAccess = await loaders.group_access.load(
        (group.name, modified_email)
    )
    # Validate role requirements before changing anything
    validate_role_fluid_reqs(modified_email, modified_role)

    invitation = group_access.invitation
    if invitation and not invitation.is_used:
        await stakeholders_domain.update_invited_stakeholder(
            updated_data, invitation, group
        )
    else:
        if await authz.grant_group_level_role(
            loaders, modified_email, group.name, modified_role
        ):
            await stakeholders_domain.update_information(
                info.context, updated_data, group.name
            )
        else:
            LOGGER.error(
                "Couldn't update stakeholder role",
                extra={"extra": info.context},
            )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    **updated_data: str,
) -> UpdateStakeholderPayloadType:
    group_name: str = updated_data["group_name"].lower()
    modified_role: str = map_roles(updated_data["role"])
    modified_email: str = updated_data["email"]

    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    allowed_roles_to_grant = (
        await authz.get_group_level_roles_a_user_can_grant(
            group=group_name,
            requester_email=user_email,
        )
    )

    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(group_name)
    await authz.validate_fluidattacks_staff_on_group(
        group, modified_email, modified_role
    )

    if modified_role in allowed_roles_to_grant:
        await _update_stakeholder(info, updated_data, group)
    else:
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

    await redis_del_by_deps("update_group_stakeholder", group_name=group_name)
    msg = (
        f"Security: Modified stakeholder data: {modified_email} "
        f"in {group_name} group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return UpdateStakeholderPayloadType(
        success=True,
        modified_stakeholder=dict(group_name=group_name, email=modified_email),
    )
