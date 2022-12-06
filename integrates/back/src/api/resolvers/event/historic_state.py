from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
    EventState,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


def _format_state_item(state: EventState) -> dict[str, str]:
    item = {
        "analyst": state.modified_by,
        "date": datetime_utils.get_as_str(state.modified_date),
        "state": state.status.value,
    }
    if state.other:
        item["other"] = state.other
    if state.reason:
        item["reason"] = state.reason.value

    return item


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, str]]:
    loaders: Dataloaders = info.context.loaders
    state: tuple[EventState, ...] = await loaders.event_historic_state.load(
        parent.id
    )
    historic_state = list(_format_state_item(item) for item in state)

    return historic_state
