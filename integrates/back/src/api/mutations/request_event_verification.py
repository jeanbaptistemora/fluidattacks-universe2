# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    stakeholders as stakeholders_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    comments: str,
    event_id: str,
    **_kwargs: Any,
) -> SimplePayload:
    stakeholder_info: Dict[str, str] = await token_utils.get_jwt_content(
        info.context
    )
    await events_domain.request_verification(
        info,
        loaders=info.context.loaders,
        event_id=event_id,
        comments=comments,
        stakeholder_email=str(stakeholder_info["user_email"]),
        stakeholder_full_name=stakeholders_utils.get_full_name(
            stakeholder_info
        ),
    )

    redis_del_by_deps_soon("request_event_verification", event_id=event_id)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Requested verification in event {event_id} successfully",
    )

    return SimplePayload(success=True)
