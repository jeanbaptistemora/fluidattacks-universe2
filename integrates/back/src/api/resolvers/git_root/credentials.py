from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credential,
    CredentialRequest,
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
) -> Optional[Credential]:
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(parent.group_name)
    if parent.state.credential_id:
        request = CredentialRequest(
            id=parent.state.credential_id,
            organization_id=group.organization_id,
        )
        credential: Credential = await loaders.credential_new.load(request)
        return credential

    return None
