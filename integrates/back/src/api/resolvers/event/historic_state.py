from db_model.events.types import (
    Event,
    EventState,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.events import (
    format_state_item,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, str]]:
    state: list[
        EventState
    ] = await info.context.loaders.event_historic_state.load(parent.id)
    historic_state = list(format_state_item(item) for item in state)
    return historic_state
