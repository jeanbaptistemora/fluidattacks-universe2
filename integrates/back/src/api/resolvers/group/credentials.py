from .schema import (
    GROUP,
)
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


@GROUP.field("credentials")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Credentials | None]:
    loaders: Dataloaders = info.context.loaders
    group_roots = await loaders.group_roots.load(parent.name)
    group_credential_ids = {
        root.state.credential_id
        for root in group_roots
        if isinstance(root, GitRoot) and root.state.credential_id
    }
    group_credentials = await loaders.credentials.load_many(
        tuple(
            CredentialsRequest(
                id=credential_id,
                organization_id=parent.organization_id,
            )
            for credential_id in group_credential_ids
        )
    )

    return group_credentials
