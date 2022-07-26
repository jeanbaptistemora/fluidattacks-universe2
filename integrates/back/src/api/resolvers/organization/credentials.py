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
) -> tuple[Credentials, ...]:
    loaders: Dataloaders = info.context.loaders
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(parent.id)
    return org_credentials
