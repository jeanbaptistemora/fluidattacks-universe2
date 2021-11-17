from custom_types import (
    Group,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLinesConnection,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> ToeLinesConnection:
    loaders: Dataloaders = info.context.loaders
    response: ToeLinesConnection = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(
            group_name=parent["name"],
            after=kwargs.get("after"),
        )
    )

    return response
