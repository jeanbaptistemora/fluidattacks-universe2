from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
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
    EventType,
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
from events.types import (
    EventAttributesToUpdate,
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
    Optional,
)


@MUTATION.field("updateEvent")
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
    **kwargs: Any,
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_info = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_info["user_email"]
        event_type = (
            EventType[kwargs["event_type"]]
            if kwargs.get("event_type")
            else None
        )
        solving_reason = (
            EventSolutionReason[kwargs["solving_reason"]]
            if kwargs.get("solving_reason")
            else None
        )
        other_solving_reason: Optional[str] = kwargs.get(
            "other_solving_reason"
        )
        event = await events_domain.get_event(loaders, event_id)
        await events_domain.update_event(
            loaders=loaders,
            event_id=event_id,
            stakeholder_email=stakeholder_email,
            attributes=EventAttributesToUpdate(
                event_type=event_type,
                other_solving_reason=other_solving_reason,
                solving_reason=solving_reason,
            ),
        )

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Update an event in {event.group_name} group"
            " successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update event in group {event.group_name}",
        )
        raise

    return SimplePayload(success=True)
