from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
)


@ME.field("enrolled")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await get_stakeholder(loaders, user_email)
    return stakeholder.enrolled
