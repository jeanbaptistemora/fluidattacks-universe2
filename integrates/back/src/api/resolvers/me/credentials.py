from .schema import (
    ME,
)
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
)


@ME.field("credentials")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo
) -> list[Credentials]:
    loaders: Dataloaders = info.context.loaders
    email = str(parent["user_email"])

    return await loaders.user_credentials.load(email)
