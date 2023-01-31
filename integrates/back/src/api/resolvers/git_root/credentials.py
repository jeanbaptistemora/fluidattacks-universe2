from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo
) -> Optional[Credentials]:
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(parent.group_name)
    if parent.state.credential_id:
        request = CredentialsRequest(
            id=parent.state.credential_id,
            organization_id=group.organization_id,
        )
        return await loaders.credentials.load(request)

    return None
