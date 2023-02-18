from .schema import (
    TOE_INPUT,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_INPUT.field("bePresent")
async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return parent.state.be_present
