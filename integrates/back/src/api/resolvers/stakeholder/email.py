from .schema import (
    STAKEHOLDER,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@STAKEHOLDER.field("email")
async def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    if isinstance(parent, dict):
        email = parent["email"]
    else:
        email = parent.email
    return email
