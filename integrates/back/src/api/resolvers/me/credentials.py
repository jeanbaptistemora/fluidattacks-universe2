from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo
) -> tuple[Credentials, ...]:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    user_credentials: tuple[
        Credentials, ...
    ] = await loaders.user_credentials.load(user_email)

    return user_credentials
