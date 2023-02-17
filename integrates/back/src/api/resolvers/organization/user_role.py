from .schema import (
    ORGANIZATION,
)
import authz
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)


@ORGANIZATION.field("userRole")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    return await authz.get_organization_level_role(
        loaders, user_email, parent.id
    )
