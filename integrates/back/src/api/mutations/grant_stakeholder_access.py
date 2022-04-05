from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    StakeholderHasGroupAccess,
)
from custom_types import (
    GrantStakeholderAccessPayload,
)
from dataloaders import (
    Dataloaders,
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
from group_access.domain import (
    validate_new_invitation_time_limit,
)
from groups import (
    domain as groups_domain,
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
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    role: str,
    **query_args: str,
) -> GrantStakeholderAccessPayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    success = False
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    new_user_role = map_roles(role)
    new_user_email = query_args.get("email", "")
    new_user_responsibility = query_args.get("responsibility", "-")

    group_access = await group_access_domain.get_user_access(
        new_user_email, group_name
    )
    if group_access:
        # Stakeholder has already accepted the invitation
        if group_access["has_access"]:
            raise StakeholderHasGroupAccess()
        # Too soon to send another email invitation to the same stakeholder
        if "expiration_time" in group_access:
            validate_new_invitation_time_limit(group_access["expiration_time"])

    allowed_roles_to_grant = (
        await authz.get_group_level_roles_a_user_can_grant(
            group=group_name,
            requester_email=user_email,
        )
    )

    if new_user_role in allowed_roles_to_grant:
        success = await groups_domain.invite_to_group(
            loaders=loaders,
            email=new_user_email,
            responsibility=new_user_responsibility,
            role=new_user_role,
            group_name=group_name,
            modified_by=user_email,
        )
    else:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "new_user_role": new_user_role,
                    "group_name": group_name,
                    "requester_email": user_email,
                }
            },
        )

    if success:
        await redis_del_by_deps(
            "grant_stakeholder_access",
            group_name=group_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Given grant access to {new_user_email} "
            f"in {group_name} group",
        )
    else:
        LOGGER.error(
            "Couldn't grant access to group", extra={"extra": info.context}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to grant access to {new_user_email} "
            f"in {group_name} group",
        )

    return GrantStakeholderAccessPayload(
        success=success,
        granted_stakeholder=dict(group_name=group_name, email=new_user_email),
    )
