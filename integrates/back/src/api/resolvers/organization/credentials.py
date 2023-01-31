from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Credentials]:
    loaders: Dataloaders = info.context.loaders
    return await loaders.organization_credentials.load(parent.id)
