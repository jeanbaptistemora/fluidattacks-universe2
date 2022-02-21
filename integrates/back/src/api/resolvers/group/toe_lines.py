from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Group,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    RootToeLinesRequest,
    ToeLinesConnection,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(enforce_group_level_auth_async, validate_connection)
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> ToeLinesConnection:
    loaders: Dataloaders = info.context.loaders
    if kwargs.get("root_id") is not None:
        response: ToeLinesConnection = await loaders.root_toe_lines.load(
            RootToeLinesRequest(
                group_name=parent["name"],
                root_id=kwargs["root_id"],
                after=kwargs.get("after"),
                be_present=kwargs.get("be_present"),
                first=kwargs.get("first"),
                paginate=True,
            )
        )
        return response

    response = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(
            group_name=parent["name"],
            after=kwargs.get("after"),
            be_present=kwargs.get("be_present"),
            first=kwargs.get("first"),
            paginate=True,
        )
    )
    return response
