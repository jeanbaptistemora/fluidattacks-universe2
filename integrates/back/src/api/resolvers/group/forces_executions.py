from datetime import (
    datetime,
)
from db_model.forces.types import (
    ExecutionEdge,
    ExecutionsConnection,
)
from db_model.forces.utils import (
    format_forces_execution,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.forces import (
    format_forces_to_resolve,
)
from search.operations import (
    search,
)
from typing import (
    Any,
    Dict,
    List,
)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> ExecutionsConnection:
    group_name: str = parent.name
    executions_filters: Dict[str, Any] = executions_filter(**kwargs)

    after = kwargs.get("after")
    first = kwargs.get("first", 10)
    query = kwargs.get("search")

    results = await search(
        after=after,
        limit=first,
        query=query,
        must_filters=executions_filters["must_filters"],
        must_match_prefix_filters=executions_filters[
            "must_match_prefix_filters"
        ],
        range_filters=executions_filters["must_range_filters"],
        exact_filters={"group_name": group_name},
        index="forces_executions",
    )

    forces_executions = tuple(
        format_forces_execution(item) for item in results.items
    )
    executions_formatted = [
        format_forces_to_resolve(execution) for execution in forces_executions
    ]
    return ExecutionsConnection(
        edges=tuple(
            ExecutionEdge(
                cursor=results.page_info.end_cursor,
                node=execution,
            )
            for execution in executions_formatted
        ),
        page_info=results.page_info,
        total=results.total,
    )


def executions_filter(**kwargs: Any) -> Dict[str, Any]:
    exec_must_filters: List[Dict[str, Any]] = must_filter(**kwargs)
    exec_must_match_prefix_filters: List[
        Dict[str, Any]
    ] = must_match_prefix_filter(**kwargs)
    exec_must_range_filters: List[Dict[str, Any]] = must_range_filter(**kwargs)

    filters: Dict[str, Any] = {
        "must_filters": exec_must_filters,
        "must_match_prefix_filters": exec_must_match_prefix_filters,
        "must_range_filters": exec_must_range_filters,
    }

    return filters


def must_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    must_filters = []

    if execution_type := kwargs.get("type"):
        must_filters.append({"kind": str(execution_type).upper()})

    return must_filters


def must_match_prefix_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    must_match_filters = []

    if repo := kwargs.get("gitRepo"):
        must_match_filters.append({"repo": str(repo)})

    return must_match_filters


def must_range_filter(**kwargs: datetime) -> List[Dict[str, Any]]:
    must_range_filters = []

    if from_date := kwargs.get("fromDate"):
        must_range_filters.append(
            {"execution_date": {"gte": str(from_date.date())}}
        )

    return must_range_filters
