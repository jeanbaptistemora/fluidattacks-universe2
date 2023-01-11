from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidBePresentFilterCursor,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
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
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> Optional[ToeLinesConnection]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    if root_id := kwargs.get("root_id"):
        response: Optional[
            ToeLinesConnection
        ] = await loaders.root_toe_lines.load(
            RootToeLinesRequest(
                group_name=group_name,
                root_id=root_id,
                after=kwargs.get("after"),
                be_present=kwargs.get("be_present"),
                first=kwargs.get("first"),
                paginate=True,
            )
        )
        if response:
            return response
        raise InvalidBePresentFilterCursor()

    response = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(
            group_name=group_name,
            after=kwargs.get("after"),
            be_present=kwargs.get("be_present"),
            first=kwargs.get("first"),
            paginate=True,
        )
    )
    return response


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_filters = []

    if be_present := kwargs.get("be_present"):
        must_filters.append({"be_present": be_present})

    if root_id := kwargs.get("root_id"):
        must_filters.append({"root_id": root_id})

    return must_filters
