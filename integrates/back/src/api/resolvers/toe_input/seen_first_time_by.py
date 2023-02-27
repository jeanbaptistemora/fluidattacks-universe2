from .schema import (
    TOE_INPUT,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_INPUT.field("seenFirstTimeBy")
@enforce_group_level_auth_async
def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.state.seen_first_time_by
