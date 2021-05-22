import logging
import logging.config
from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

import authz
from back.settings import LOGGING
from custom_exceptions import StakeholderHasGroupAccess
from custom_types import (
    GrantStakeholderAccessPayload as GrantStakeholderAccessPayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import redis_del_by_deps


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, role: str, **query_args: str
) -> GrantStakeholderAccessPayloadType:
    project_name = query_args.get("project_name", "").lower()
    success = False
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    new_user_role = role
    new_user_email = query_args.get("email", "")
    new_user_responsibility = query_args.get("responsibility", "-")

    project_access = await group_access_domain.get_user_access(
        new_user_email, project_name
    )
    if project_access and project_access["has_access"]:
        raise StakeholderHasGroupAccess()

    allowed_roles_to_grant = (
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )
    )

    if new_user_role in allowed_roles_to_grant:
        success = await groups_domain.invite_to_group(
            email=new_user_email,
            responsibility=new_user_responsibility,
            role=new_user_role,
            phone_number=query_args.get("phone_number", ""),
            group_name=project_name,
        )
    else:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "new_user_role": new_user_role,
                    "project_name": project_name,
                    "requester_email": user_email,
                }
            },
        )

    if success:
        await redis_del_by_deps(
            "grant_stakeholder_access",
            group_name=project_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Given grant access to {new_user_email} "
            f"in {project_name} project",
        )
    else:
        LOGGER.error(
            "Couldn't grant access to project", extra={"extra": info.context}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to grant access to {new_user_email} "
            f"in {project_name} project",
        )

    return GrantStakeholderAccessPayloadType(
        success=success,
        granted_stakeholder=dict(
            project_name=project_name, email=new_user_email
        ),
    )
