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
    evidence_file: Optional[str] = (
        parent.evidences.file.file_name if parent.evidences.file else None
    )
    return evidence_file
