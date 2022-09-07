# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.forces.types import (
    ForcesExecution,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], ForcesExecution],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    if isinstance(parent, dict):
        group_name: str = get_key_or_fallback(parent)
        execution_id = str(parent["execution_id"])
    else:
        group_name = parent.group_name
        execution_id = parent.id

    return await forces_domain.get_log_execution(group_name, execution_id)
