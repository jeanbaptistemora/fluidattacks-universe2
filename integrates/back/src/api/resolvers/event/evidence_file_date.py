from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    if not parent.evidences.file_1:
        return None
    return convert_from_iso_str(parent.evidences.file_1.modified_date)
