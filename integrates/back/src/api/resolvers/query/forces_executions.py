# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.forces.utils import (
    format_forces_execution,
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
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: Any
) -> dict[str, Any]:
    group_name: str = kwargs["group_name"]

    results = await search(
        exact_filters={"group_name": group_name},
        index="forces_executions",
        limit=200,
    )

    forces_executions = tuple(
        format_forces_execution(item) for item in results.items
    )
    executions_formatted = [
        format_forces_to_resolve(execution) for execution in forces_executions
    ]
    return {
        "executions": executions_formatted,
        "group_name": group_name,
    }
