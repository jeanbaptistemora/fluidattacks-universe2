from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@QUERY.field("organization")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Optional[Organization]:
    loaders: Dataloaders = info.context.loaders
    organization_id: str = kwargs["organization_id"]

    return await loaders.organization.load(organization_id)
