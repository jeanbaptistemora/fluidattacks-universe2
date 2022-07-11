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
    solving_date = parent.unreliable_indicators.unreliable_solving_date
    if solving_date:
        closing_date = convert_from_iso_str(solving_date)
    else:
        closing_date = "-"
    return closing_date
