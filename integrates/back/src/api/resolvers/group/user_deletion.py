# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> Optional[str]:
    return (
        parent.state.modified_by
        if parent.state.status == GroupStateStatus.DELETED
        else None
    )
