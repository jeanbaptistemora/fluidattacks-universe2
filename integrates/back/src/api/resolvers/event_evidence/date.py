# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.events.types import (
    EventEvidence,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
)
from typing import (
    Optional,
)


async def resolve(
    parent: EventEvidence,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    return convert_from_iso_str(parent.modified_date)
