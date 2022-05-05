from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    Credential,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Credential]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name

    return [
        Credential(
            id=root_cred.id,
            name=root_cred.state.name,
            type=root_cred.metadata.type,
        )
        for root_cred in await loaders.group_credentials.load(group_name)
    ]
