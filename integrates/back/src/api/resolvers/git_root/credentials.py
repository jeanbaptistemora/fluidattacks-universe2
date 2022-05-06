from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    Credential,
)


async def resolve(parent: GitRoot, info: GraphQLResolveInfo) -> Credential:
    creds_loader = info.context.loaders.group_credentials
    group_creds = await creds_loader.load(parent.group_name)
    root_cred = next(
        filter(lambda x: parent.id in x.state.roots, group_creds), None
    )
    if root_cred:
        return Credential(
            id=root_cred.id,
            name=root_cred.state.name,
            type=root_cred.metadata.type,
        )
    return Credential(id="", name="", type="")
