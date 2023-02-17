from datetime import (
    datetime,
)
from db_model.events.types import (
    EventEvidence,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: EventEvidence,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[datetime]:
    return parent.modified_date
