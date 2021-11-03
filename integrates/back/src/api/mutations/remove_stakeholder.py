from aioextensions import (
    collect,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups.domain import (
    get_groups_by_user,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations.domain import (
    get_user_organizations,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from remove_user.domain import (
    remove_user_all_organizations,
)
from sessions.dal import (
    remove_session_key,
)
from typing import (
    Any,
)


@require_login
async def mutate(_: Any, info: GraphQLResolveInfo) -> SimplePayloadType:
    stakeholder_info = await token_utils.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    stakeholder_organizations_ids = await get_user_organizations(
        stakeholder_email
    )
    stakeholder_groups = await get_groups_by_user(stakeholder_email)
    await remove_user_all_organizations(email=stakeholder_email)

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_organization_access",
                organization_id=organization_id,
            )
            for organization_id in stakeholder_organizations_ids
        )
    )

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_access",
                group_name=group_name,
            )
            for group_name in stakeholder_groups
        )
    )

    msg = f"Security: Removed stakeholder: {stakeholder_email}"
    logs_utils.cloudwatch_log(info.context, msg)

    await collect(
        [
            remove_session_key(stakeholder_email, "jti"),
            remove_session_key(stakeholder_email, "web"),
            remove_session_key(stakeholder_email, "jwt"),
        ]
    )

    return SimplePayloadType(success=True)
