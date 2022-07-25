from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.events.enums import (
    EventAffectedComponents,
    EventType,
)
from db_model.events.types import (
    Event,
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
    **kwargs: Any,
) -> SimplePayload:
    try:
        event_type = (
            EventType[kwargs["event_type"]] if "event_type" in kwargs else None
        )
        affected_components = (
            set(
                EventAffectedComponents[item]
                for item in kwargs["affected_components"]
                if item
            )
            if "affected_components" in kwargs
            else None
        )
        event: Event = await info.context.loaders.event.load(event_id)
        await events_domain.update_event(
            loaders=info.context.loaders,
            event_id=event_id,
            attributes=EventAttributesToUpdate(
                event_type=event_type, affected_components=affected_components
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
