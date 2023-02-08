from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return parent.state.be_present
