from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderTours,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> StakeholderTours:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    return stakeholder.tours
