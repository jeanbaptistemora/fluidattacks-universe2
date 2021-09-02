from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_types import (
    Invitation as InvitationType,
    UpdateStakeholderPayload as UpdateStakeholderPayloadType,
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
from group_access import (
    domain as group_access_domain,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
    map_roles,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
)
from users import (
    domain as users_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _update_stakeholder(
    info: GraphQLResolveInfo, updated_data: Dict[str, str]
) -> bool:
    success = False
    group_name: str = get_key_or_fallback(updated_data).lower()
    modified_role = map_roles(updated_data["role"])
    modified_email = updated_data["email"]
    group_access = await group_access_domain.get_user_access(
        modified_email, group_name
    )
    if group_access:
        invitation = cast(InvitationType, group_access.get("invitation"))
        if invitation and not invitation["is_used"]:
            success = await users_domain.update_invited_stakeholder(
                updated_data, invitation, group_name
            )
        else:
            if await authz.grant_group_level_role(
                modified_email, group_name, modified_role
            ):
                success = await users_domain.update_user_information(
                    info.context, updated_data, group_name
                )
            else:
                LOGGER.error(
                    "Couldn't update stakeholder role",
                    extra={"extra": info.context},
                )
    else:
        raise StakeholderNotFound()

    return success


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **updated_data: str
) -> UpdateStakeholderPayloadType:
    group_name: str = get_key_or_fallback(updated_data).lower()
    modified_role: str = map_roles(updated_data["role"])
    modified_email: str = updated_data["email"]

    success = False
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    allowed_roles_to_grant = (
        await authz.get_group_level_roles_a_user_can_grant(
            group=group_name,
            requester_email=user_email,
        )
    )

    await authz.validate_fluidattacks_staff_on_group(
        group_name, modified_email, modified_role
    )

    if modified_role in allowed_roles_to_grant:
        success = await _update_stakeholder(info, updated_data)
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

    if success:
        await redis_del_by_deps(
            "update_group_stakeholder", group_name=group_name
        )
        msg = (
            f"Security: Modified stakeholder data: {modified_email} "
            f"in {group_name} group successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f"Security: Attempted to modify stakeholder "
            f"data:{modified_email} in "
            f"{group_name} group"
        )
        logs_utils.cloudwatch_log(info.context, msg)

    return UpdateStakeholderPayloadType(
        success=success,
        modified_stakeholder=dict(
            group_name=group_name, email=updated_data["email"]
        ),
    )
