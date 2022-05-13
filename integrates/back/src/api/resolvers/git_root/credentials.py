from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    Credential,
)
from typing import (
    Any,
    Optional,
)


@enforce_group_level_auth_async
async def get_credentials_value(
    parent: GitRoot,  # pylint: disable=unused-argument
    info: GraphQLResolveInfo,  # pylint: disable=unused-argument
    cred: Any,
) -> dict[str, Optional[str]]:
    return {
        "key": cred.state.key,
        "user": cred.state.user,
        "password": cred.state.password,
        "token": cred.state.token,
    }


async def resolve(parent: GitRoot, info: GraphQLResolveInfo) -> Credential:
    creds_loader = info.context.loaders.group_credentials
    group_creds = await creds_loader.load(parent.group_name)
    root_cred = next(
        filter(lambda x: parent.id in x.state.roots, group_creds), None
    )
    requested_fields: list[str] = [
        item.name.value
        for item in info.field_nodes[0].selection_set.selections
    ]
    cred_values: dict[str, Optional[str]] = {}
    if (
        root_cred is not None
        and len(
            {"key", "user", "password", "token"}.intersection(requested_fields)
        )
        > 0
    ):
        cred_values = await get_credentials_value(parent, info, root_cred)

    if root_cred:
        return Credential(
            id=root_cred.id,
            name=root_cred.state.name,
            type=root_cred.metadata.type,
            **cred_values,
        )
    return Credential(id="", name="", type="")
