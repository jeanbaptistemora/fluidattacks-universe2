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
    toe_lines_filters: dict[str, Any] = toe_lines_filter(**kwargs)

    results = await search(
        after=kwargs.get("after"),
        exact_filters={"group_name": parent.name},
        must_filters=toe_lines_filters["must_filters"],
        must_match_prefix_filters=toe_lines_filters["must_match_filters"],
        range_filters=toe_lines_filters["must_range_filters"],
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


def toe_lines_filter(**kwargs: Any) -> dict[str, Any]:
    vulns_must_filters: list[dict[str, Any]] = must_filter(**kwargs)
    vulns_must_match_prefix_filters: list[
        dict[str, Any]
    ] = must_match_prefix_filter(**kwargs)
    exec_must_range_filters: list[dict[str, Any]] = must_range_filter(**kwargs)

    filters: dict[str, Any] = {
        "must_filters": vulns_must_filters,
        "must_match_filters": vulns_must_match_prefix_filters,
        "must_range_filters": exec_must_range_filters,
    }

    return filters


def get_items_to_filter(
    filters: dict[str, Any],
    kwargs: Any,
) -> list[dict[str, Any]]:
    items_to_filter = [
        {(field if path == "common" else f"{path}.{field}"): kwargs.get(field)}
        for path, fields in filters.items()
        for field in fields
        if kwargs.get(field)
    ]
    return items_to_filter


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    filters: dict[str, Any] = {
        "common": ["root_id"],
        "state": ["be_present", "has_vulnerabilities"],
    }
    must_filters = get_items_to_filter(filters, kwargs)

    return must_filters


def must_match_prefix_filter(**kwargs: Any) -> list[dict[str, Any]]:
    filters: dict[str, Any] = {
        "common": ["filename"],
        "state": ["attacked_by", "comments", "last_commit", "last_author"],
    }

    must_match_filters = get_items_to_filter(filters, kwargs)

    return must_match_filters


def must_range_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_range_filters: list[dict[str, Any]] = []

    if min_loc := kwargs.get("min_loc"):
        must_range_filters.append({"state.loc": {"gte": min_loc}})

    if max_loc := kwargs.get("max_loc"):
        must_range_filters.append({"state.loc": {"lte": max_loc}})

    if min_attacked_lines := kwargs.get("min_attacked_lines"):
        must_range_filters.append(
            {"state.attacked_lines": {"gte": min_attacked_lines}}
        )

    if max_attacked_lines := kwargs.get("max_attacked_lines"):
        must_range_filters.append(
            {"state.attacked_lines": {"lte": max_attacked_lines}}
        )

    if from_modified_date := kwargs.get("from_modified_date"):
        must_range_filters.append(
            {"modified_date": {"gte": str(from_modified_date.date())}}
        )

    if to_modified_date := kwargs.get("to_modified_date"):
        must_range_filters.append(
            {"modified_date": {"lte": str(to_modified_date.date())}}
        )

    if from_seen_at := kwargs.get("from_seen_at"):
        must_range_filters.append(
            {"state.seen_at": {"gte": str(from_seen_at.date())}}
        )

    if to_seen_at := kwargs.get("to_seen_at"):
        must_range_filters.append(
            {"state.seen_at": {"lte": str(to_seen_at.date())}}
        )

    return must_range_filters
