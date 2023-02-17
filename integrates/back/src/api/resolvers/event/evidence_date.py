from .schema import (
    EVENT,
)
from datetime import (
    datetime,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@EVENT.field("evidenceDate")
async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[datetime]:
    if not parent.evidences.image_1:
        return None
    return parent.evidences.image_1.modified_date
