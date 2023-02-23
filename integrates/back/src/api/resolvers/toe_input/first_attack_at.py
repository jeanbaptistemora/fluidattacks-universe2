from .schema import (
    TOE_INPUT,
)
from datetime import (
    datetime,
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


@TOE_INPUT.field("firstAttackAt")
@enforce_group_level_auth_async
async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> datetime | None:
    return parent.state.first_attack_at
