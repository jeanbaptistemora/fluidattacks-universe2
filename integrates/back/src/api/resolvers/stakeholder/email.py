from .schema import (
    STAKEHOLDER,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@STAKEHOLDER.field("email")
async def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    if isinstance(parent, dict):
        email = parent["email"]
    else:
        email = parent.email
    return email
