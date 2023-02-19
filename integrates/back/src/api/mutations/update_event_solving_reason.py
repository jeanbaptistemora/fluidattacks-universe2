from .payloads.types import (
    SimplePayload,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventSolutionReason,
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
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
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
    event_id: str,
    reason: str,
    **kwargs: Any,
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_info = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_info["user_email"]
        other = kwargs.get("other")
        await events_domain.update_solving_reason(
            loaders=loaders,
            event_id=event_id,
            stakeholder_email=stakeholder_email,
            reason=EventSolutionReason[reason],
            other=other,
        )
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Update event solving reason in"
            f" {event_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update event solving reason in"
            f" {event_id}",
        )
        raise

    return SimplePayload(success=True)
