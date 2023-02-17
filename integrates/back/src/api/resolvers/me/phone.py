from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
    Dict,
    Optional,
)


@ME.field("phone")
async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[StakeholderPhone]:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await get_stakeholder(loaders, user_email)
    return stakeholder.phone
