from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
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
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("rejectEventSolution")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    comments: str,
    event_id: str,
    **_kwargs: Any,
) -> SimplePayload:
    stakeholder_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    await events_domain.reject_solution(
        loaders=info.context.loaders,
        event_id=event_id,
        comments=comments,
        stakeholder_email=str(stakeholder_info["user_email"]),
        stakeholder_full_name=stakeholders_utils.get_full_name(
            stakeholder_info
        ),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Rejected solution in event {event_id} successfully",
    )

    return SimplePayload(success=True)
