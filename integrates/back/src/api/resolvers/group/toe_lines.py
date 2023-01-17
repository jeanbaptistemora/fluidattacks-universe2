from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_lines.types import (
    ToeLinesConnection,
    ToeLinesEdge,
)
from db_model.toe_lines.utils import (
    format_toe_lines,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.operations import (
    search,
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
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> Optional[ToeLinesConnection]:
    must_filters: list[dict[str, Any]] = must_filter(**kwargs)

    results = await search(
        after=kwargs.get("after"),
        exact_filters={"group_name": parent.name},
        must_filters=must_filters,
        index="toe_lines",
        limit=kwargs.get("first", 10),
    )

    toe_lines = tuple(format_toe_lines(result) for result in results.items)

    response = ToeLinesConnection(
        edges=tuple(
            ToeLinesEdge(
                cursor=results.page_info.end_cursor,
                node=toe_line,
            )
            for toe_line in toe_lines
        ),
        page_info=results.page_info,
        total=results.total,
    )
    return response


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_filters = []

    if be_present := kwargs.get("be_present"):
        must_filters.append({"be_present": be_present})

    if root_id := kwargs.get("root_id"):
        must_filters.append({"root_id": root_id})

    return must_filters
