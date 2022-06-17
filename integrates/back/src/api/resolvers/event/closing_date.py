from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
)


async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    if parent.state.status == EventStateStatus.SOLVED:
        closing_date = convert_from_iso_str(parent.state.modified_date)
    else:
        closing_date = "-"
    return closing_date
