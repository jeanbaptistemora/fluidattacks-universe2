from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[datetime]:
    return parent.state.seen_at
