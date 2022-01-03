from db_model.toe_inputs.types import (
    ToeInput,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.first_attack_at
