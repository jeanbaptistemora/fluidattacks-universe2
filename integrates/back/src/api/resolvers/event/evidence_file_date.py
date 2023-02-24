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


@EVENT.field("evidenceFileDate")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> datetime | None:
    if not parent.evidences.file_1:
        return None
    return parent.evidences.file_1.modified_date
