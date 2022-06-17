from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    evidence = (
        parent.evidences.image.file_name if parent.evidences.image else None
    )
    return evidence
