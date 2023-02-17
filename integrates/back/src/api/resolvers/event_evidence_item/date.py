from .schema import (
    EVENT_EVIDENCE_ITEM,
)
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


@EVENT_EVIDENCE_ITEM.field("date")
async def resolve(
    parent: EventEvidence,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[datetime]:
    return parent.modified_date
