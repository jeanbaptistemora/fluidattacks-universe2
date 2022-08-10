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
from newutils import (
    token as token_utils,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: dict[str, str],
) -> str:
    loaders: Dataloaders = info.context.loaders
    organization_id = str(kwargs.get("identifier", parent.id))
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await authz.get_organization_level_role(
        loaders, user_email, organization_id
    )
