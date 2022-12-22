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
from search.enums import (
    Sort,
)
from search.operations import (
    search,
)
from typing import (
    Any,
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

    after = kwargs.get("after")
    first = kwargs.get("first", 10)
    query = kwargs.get("search")

    results = await search(
        after=after,
        limit=first,
        query=query,
        exact_filters={"group_name": group_name},
        index="forces_executions",
        sort_by={"execution_date": Sort.DESCENDING.value},
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
