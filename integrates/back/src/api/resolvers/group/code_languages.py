# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from db_model.types import (
    CodeLanguage,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
    Optional,
)


@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[List[CodeLanguage]]:
    loaders: Dataloaders = info.context.loaders
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(parent.name)
    )
    return group_indicators.code_languages
