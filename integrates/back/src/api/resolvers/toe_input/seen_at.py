from .schema import (
    TOE_INPUT,
)
from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_INPUT.field("seenAt")
def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> datetime | None:
    return parent.state.seen_at
